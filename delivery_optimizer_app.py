from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple
import time
import random
import math

# --- DATA MODELS ---

class VehicleType(Enum):
    BIKE = "Bike"
    VAN = "Van"
    TRUCK = "Truck"

class DeliveryStatus(Enum):
    PENDING = "Pending"
    ASSIGNED = "Assigned"
    DELIVERED = "Delivered"

@dataclass
class Location:
    id: str
    latitude: float
    longitude: float
    address: str
    name: str = ""

@dataclass
class TimeWindow:
    start_time: int  # e.g., 900 for 9:00 AM
    end_time: int    # e.g., 1700 for 5:00 PM

@dataclass
class Delivery:
    id: str
    location: Location
    weight: float
    priority: int  # Higher is more urgent
    time_window: TimeWindow = None
    status: DeliveryStatus = DeliveryStatus.PENDING

@dataclass
class Vehicle:
    id: str
    vehicle_type: VehicleType
    capacity_weight: float
    current_load_weight: float = 0.0
    route: List[Delivery] = field(default_factory=list)

    def get_load_percentage(self) -> float:
        if self.capacity_weight == 0: 
            return 0.0
        return (self.current_load_weight / self.capacity_weight) * 100

    def add_delivery(self, delivery: Delivery) -> bool:
        if self.current_load_weight + delivery.weight <= self.capacity_weight:
            self.route.append(delivery)
            self.current_load_weight += delivery.weight
            delivery.status = DeliveryStatus.ASSIGNED
            return True
        return False

# --- UTILITY FUNCTIONS ---

class DistanceCalculator:
    """Calculate distances between locations using Haversine formula."""
    
    EARTH_RADIUS_KM = 6371  # Earth's radius in kilometers
    
    @staticmethod
    def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two points using Haversine formula.
        Returns distance in kilometers.
        """
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return DistanceCalculator.EARTH_RADIUS_KM * c
    
    @staticmethod
    def calculate_route_distance(locations: List[Location]) -> float:
        """Calculate total distance for a route visiting locations in order."""
        if len(locations) < 2:
            return 0.0
        
        total_distance = 0.0
        for i in range(len(locations) - 1):
            total_distance += DistanceCalculator.haversine(
                locations[i].latitude, locations[i].longitude,
                locations[i + 1].latitude, locations[i + 1].longitude
            )
        return total_distance

# --- DAA ALGORITHMS ---

class ActivitySelectionOptimizer:
    """Greedy: Selects maximum non-overlapping deliveries based on time windows."""
    @staticmethod
    def optimize(deliveries: List[Delivery]) -> List[Delivery]:
        # Sort by end time
        sorted_del = sorted(deliveries, key=lambda x: x.time_window.end_time if x.time_window else 9999)
        selected = []
        last_end_time = 0
        
        for d in sorted_del:
            if d.time_window and d.time_window.start_time >= last_end_time:
                selected.append(d)
                last_end_time = d.time_window.end_time
        return selected

class FractionalKnapsackOptimizer:
    """Greedy: Maximizes the priority value per kg for a given vehicle's capacity."""
    @staticmethod
    def optimize(deliveries: List[Delivery], capacity: float) -> Tuple[List[Delivery], float]:
        # Sort by value/weight ratio (priority/weight) descending
        sorted_del = sorted(deliveries, key=lambda x: x.priority / x.weight if x.weight > 0 else 0, reverse=True)
        
        selected = []
        total_weight = 0.0
        
        for d in sorted_del:
            if total_weight + d.weight <= capacity:
                selected.append(d)
                total_weight += d.weight
        return selected, total_weight

class MaxSumSubarrayOptimizer:
    """DP (Kadane's): Finds a sequence of adjacent deliveries with the highest combined priority."""
    @staticmethod
    def optimize(deliveries: List[Delivery]) -> Tuple[List[Delivery], int]:
        if not deliveries: return [], 0
        
        max_so_far = float('-inf')
        current_max = 0
        start = end = s = 0
        
        for i, d in enumerate(deliveries):
            current_max += d.priority
            if current_max > max_so_far:
                max_so_far = current_max
                start = s
                end = i
            if current_max < 0:
                current_max = 0
                s = i + 1
                
        return deliveries[start:end+1], max_so_far

class LCSRouteValidator:
    """DP: Validates planned route against actual route using Longest Common Subsequence."""
    @staticmethod
    def validate(planned: List[str], actual: List[str]) -> int:
        m, n = len(planned), len(actual)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if planned[i-1] == actual[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        return dp[m][n]

# --- MAIN ORCHESTRATOR ---

class DeliveryOptimizer:
    def __init__(self, depot: Location):
        self.depot = depot
        self.vehicles: List[Vehicle] = []
        self.deliveries: List[Delivery] = []

    def add_vehicle(self, vehicle: Vehicle):
        self.vehicles.append(vehicle)

    def add_delivery(self, delivery: Delivery):
        self.deliveries.append(delivery)

    def optimize_routes(self) -> Dict[str, Any]:
        start_time = time.perf_counter()
        
        # 1. Knapsack Optimization for primary loading
        unassigned = [d for d in self.deliveries if d.status == DeliveryStatus.PENDING]
        total_knapsack_weight = 0
        knapsack_count = 0
        total_knapsack_priority = 0
        
        for vehicle in self.vehicles:
            if not unassigned: break
            # Use knapsack to get the most valuable cargo that fits
            selected, weight = FractionalKnapsackOptimizer.optimize(unassigned, vehicle.capacity_weight)
            total_knapsack_weight += weight
            for d in selected:
                vehicle.add_delivery(d)
                unassigned.remove(d)
                total_knapsack_priority += d.priority
                knapsack_count += 1
                
        # 2. Activity Selection (Simulated for metrics)
        activity_selected = ActivitySelectionOptimizer.optimize(self.deliveries)
        
        # 3. Max Priority Cluster (Simulated for metrics)
        cluster, total_priority = MaxSumSubarrayOptimizer.optimize(self.deliveries)
        
        # 4. Calculate route distances for each vehicle
        vehicle_distances = {}
        for vehicle in self.vehicles:
            route_locations = [self.depot] + [d.location for d in vehicle.route] + [self.depot]
            distance = DistanceCalculator.calculate_route_distance(route_locations)
            vehicle_distances[vehicle.id] = distance
        
        total_distance = sum(vehicle_distances.values())
        
        end_time = time.perf_counter()
        
        return {
            "compute_time_ms": (end_time - start_time) * 1000,
            "summary": {
                "activity_selection": {"count": len(activity_selected)},
                "fractional_knapsack": {
                    "count": knapsack_count, 
                    "total_weight": total_knapsack_weight,
                    "total_priority": total_knapsack_priority
                },
                "max_priority_cluster": {"count": len(cluster), "total_priority": total_priority}
            },
            "route_metrics": {
                "total_distance_km": total_distance,
                "vehicle_distances": vehicle_distances,
                "average_distance_per_vehicle": total_distance / len(self.vehicles) if self.vehicles else 0
            }
        }

# --- SAMPLE DATA GENERATOR ---

def create_sample_data(num_vehicles=3, min_weight=20, max_weight=150, 
                       min_capacity=300, max_capacity=1200, min_priority=1, max_priority=10):
    """
    Generate sample data with customizable parameters.
    
    Args:
        num_vehicles: Number of vehicles to create
        min_weight: Minimum parcel weight (kg)
        max_weight: Maximum parcel weight (kg)
        min_capacity: Minimum vehicle capacity (kg)
        max_capacity: Maximum vehicle capacity (kg)
        min_priority: Minimum priority level
        max_priority: Maximum priority level
    """
    depot = Location("DEP01", 19.0760, 72.8777, "Mumbai Port")
    
    # Vehicle types for variety
    vehicle_types = [VehicleType.VAN, VehicleType.TRUCK, VehicleType.BIKE]
    
    vehicles = []
    for i in range(num_vehicles):
        vehicle_type = vehicle_types[i % len(vehicle_types)]
        capacity = random.uniform(min_capacity, max_capacity)
        vehicles.append(Vehicle(f"V-{i+1:02d}", vehicle_type, capacity_weight=capacity))
    
    addresses = [
        "Andheri West", "Bandra Kurla Complex", "Colaba", "Dadar", 
        "Juhu", "Powai", "Worli", "Malad", "Borivali", "Goregaon",
        "Vile Parle", "Chembur", "Kurla", "Santacruz", "Sion",
        "Thane", "Navi Mumbai", "Pune", "Deccan", "Wakad"
    ]
    
    deliveries = []
    for i in range(15):
        deliv = Delivery(
            id=f"DEL-{1000+i}",
            location=Location(f"LOC{i}", 19.0 + (i*0.01), 72.8 + (i*0.01), addresses[i]),
            weight=random.uniform(min_weight, max_weight),
            priority=random.randint(min_priority, max_priority),
            time_window=TimeWindow(900 + (i*100), 1200 + (i*100))
        )
        deliveries.append(deliv)
        
    return depot, vehicles, deliveries