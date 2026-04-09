"""
Delivery Route Optimizer - Professional Web Application
Flask Backend + Modern HTML/CSS/JavaScript Frontend
"""

from flask import Flask, render_template_string, request, jsonify
from delivery_optimizer_app import (
    DeliveryOptimizer, Location, Vehicle, Delivery, TimeWindow, VehicleType,
    ActivitySelectionOptimizer, FractionalKnapsackOptimizer,
    MaxSumSubarrayOptimizer, LCSRouteValidator, create_sample_data
)
from datetime import datetime, timedelta
import json

app = Flask(__name__)

# HTML Template - Modern UI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Delivery Route Optimizer</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
            animation: slideDown 0.6s ease;
        }

        header h1 {
            font-size: 48px;
            font-weight: 700;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        header p {
            font-size: 18px;
            opacity: 0.9;
        }

        .main-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }

        .card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            animation: slideUp 0.6s ease;
        }

        .card h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 24px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 600;
            font-size: 14px;
        }

        input[type="text"],
        input[type="number"],
        select {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            transition: all 0.3s ease;
        }

        input[type="text"]:focus,
        input[type="number"]:focus,
        select:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .button-group {
            display: flex;
            gap: 10px;
            margin-top: 20px;
        }

        button {
            flex: 1;
            padding: 12px 20px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        }

        .btn-secondary {
            background: #f5f5f5;
            color: #333;
        }

        .btn-secondary:hover {
            background: #e0e0e0;
        }

        .results-container {
            grid-column: 1 / -1;
        }

        .algorithm-results {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .algorithm-card {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 12px;
            padding: 20px;
            border-left: 5px solid #667eea;
        }

        .algorithm-card.activity {
            border-left-color: #FF6B6B;
        }

        .algorithm-card.knapsack {
            border-left-color: #4ECDC4;
        }

        .algorithm-card.maxsum {
            border-left-color: #95E1D3;
        }

        .algorithm-card.lcs {
            border-left-color: #FFE66D;
        }

        .algorithm-name {
            font-weight: 700;
            color: #333;
            margin-bottom: 10px;
            font-size: 16px;
        }

        .algorithm-stat {
            display: flex;
            justify-content: space-between;
            margin: 8px 0;
            font-size: 14px;
        }

        .stat-label {
            color: #666;
        }

        .stat-value {
            font-weight: 600;
            color: #333;
        }

        .fleet-summary {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }

        .fleet-item {
            background: white;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }

        .vehicle-name {
            font-weight: 700;
            color: #333;
            margin-bottom: 8px;
        }

        .vehicle-stat {
            display: flex;
            justify-content: space-between;
            font-size: 13px;
            margin: 5px 0;
            color: #666;
        }

        .metric-badge {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 12px;
            margin: 2px;
        }

        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }

        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }

        .metric-value {
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 5px;
        }

        .metric-label {
            font-size: 12px;
            opacity: 0.9;
        }

        .loading {
            display: none;
            text-align: center;
            padding: 40px;
        }

        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .success-message {
            background: #4caf50;
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: none;
        }

        .error-message {
            background: #f44336;
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: none;
        }

        .tab-buttons {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            border-bottom: 2px solid #e0e0e0;
        }

        .tab-btn {
            padding: 12px 20px;
            border: none;
            background: none;
            cursor: pointer;
            font-weight: 600;
            color: #999;
            border-bottom: 3px solid transparent;
            transition: all 0.3s ease;
        }

        .tab-btn.active {
            color: #667eea;
            border-bottom-color: #667eea;
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr;
            }

            header h1 {
                font-size: 32px;
            }

            .algorithm-results {
                grid-template-columns: 1fr;
            }
        }

        .footer {
            text-align: center;
            color: white;
            margin-top: 40px;
            opacity: 0.8;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }

        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }

        th {
            background: #667eea;
            color: white;
            font-weight: 600;
        }

        tr:hover {
            background: #f5f5f5;
        }

        .comparison-table {
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }

        .locations-section {
            display: grid;
            gap: 20px;
        }

        .location-item {
            background: #f9f9f9;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            padding: 15px;
            display: grid;
            grid-template-columns: 1fr 1fr 1fr 0.5fr;
            gap: 10px;
            align-items: end;
        }

        .location-item input {
            margin-bottom: 0;
        }

        .location-item button {
            padding: 10px 15px;
            background: #f44336;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 12px;
        }

        .location-item button:hover {
            background: #d32f2f;
        }

        .add-location-btn {
            display: inline_block;
            padding: 12px 20px;
            background: #4caf50;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            margin-top: 10px;
        }

        .add-location-btn:hover {
            background: #45a049;
        }

        .preset-cities {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
            gap: 8px;
            margin-bottom: 15px;
        }

        .preset-city-btn {
            padding: 8px 12px;
            background: #e3f2fd;
            color: #1976d2;
            border: 2px solid #1976d2;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            font-size: 12px;
            transition: all 0.3s ease;
        }

        .preset-city-btn:hover {
            background: #1976d2;
            color: white;
        }

        .preset-city-btn.active {
            background: #1976d2;
            color: white;
        }

    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🚚 Delivery Route Optimizer</h1>
            <p>Advanced Algorithm-Based Logistics Optimization</p>
        </header>

        <div class="main-content">
            <!-- Control Panel -->
            <div class="card">
                <h2>⚙️ Configuration</h2>
                
                <div class="form-group">
                    <label>📦 Number of Parcels</label>
                    <select id="numDeliveries">
                        <option value="5">5 Parcels</option>
                        <option value="8" selected>8 Parcels</option>
                        <option value="12">12 Parcels</option>
                        <option value="15">15 Parcels</option>
                        <option value="20">20 Parcels</option>
                        <option value="30">30 Parcels</option>
                    </select>
                </div>

                <div class="form-group">
                    <label>Number of Vehicles</label>
                    <select id="numVehicles">
                        <option value="1">1 Vehicle</option>
                        <option value="2">2 Vehicles</option>
                        <option value="3" selected>3 Vehicles</option>
                        <option value="4">4 Vehicles</option>
                        <option value="5">5 Vehicles</option>
                    </select>
                </div>

                <div class="form-group">
                    <label>Depot Location</label>
                    <input type="text" id="depotLocation" value="Mumbai Port, India" placeholder="Enter depot location">
                </div>

                <div class="form-group">
                    <label>Depot Latitude</label>
                    <input type="number" id="depotLat" value="19.0760" step="0.0001" placeholder="Latitude">
                </div>

                <div class="form-group">
                    <label>Depot Longitude</label>
                    <input type="number" id="depotLon" value="72.8777" step="0.0001" placeholder="Longitude">
                </div>

                <div class="form-group">
                    <label>Parcel Weight Range (kg)</label>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                        <input type="number" id="minWeight" value="20" placeholder="Min" min="0" step="5">
                        <input type="number" id="maxWeight" value="150" placeholder="Max" min="0" step="5">
                    </div>
                </div>

                <div class="form-group">
                    <label>Vehicle Capacity Range (kg)</label>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                        <input type="number" id="minCapacity" value="300" placeholder="Min" min="0" step="50">
                        <input type="number" id="maxCapacity" value="1200" placeholder="Max" min="0" step="50">
                    </div>
                </div>

                <div class="form-group">
                    <label>Priority Range</label>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                        <input type="number" id="minPriority" value="1" placeholder="Min" min="1" max="10" step="1">
                        <input type="number" id="maxPriority" value="10" placeholder="Max" min="1" max="10" step="1">
                    </div>
                </div>

                <div class="button-group">
                    <button class="btn-primary" onclick="runOptimization()">
                        ▶️ Run Optimization
                    </button>
                    <button class="btn-secondary" onclick="resetForm()">
                        🔄 Reset
                    </button>
                </div>
            </div>

            <!-- Delivery Locations -->
            <div class="card">
                <h2>📍 Delivery Locations</h2>
                
                <label style="margin-top: 15px;">Quick Select Cities</label>
                <div class="preset-cities">
                    <button type="button" class="preset-city-btn" onclick="addPresetCity('Mumbai', 19.0760, 72.8777)">Mumbai</button>
                    <button type="button" class="preset-city-btn" onclick="addPresetCity('Delhi', 28.7041, 77.1025)">Delhi</button>
                    <button type="button" class="preset-city-btn" onclick="addPresetCity('Bangalore', 12.9716, 77.5946)">Bangalore</button>
                    <button type="button" class="preset-city-btn" onclick="addPresetCity('Chennai', 13.0827, 80.2707)">Chennai</button>
                    <button type="button" class="preset-city-btn" onclick="addPresetCity('Pune', 18.5204, 73.8567)">Pune</button>
                    <button type="button" class="preset-city-btn" onclick="addPresetCity('Hyderabad', 17.3850, 78.4867)">Hyderabad</button>
                    <button type="button" class="preset-city-btn" onclick="addPresetCity('Kolkata', 22.5726, 88.3639)">Kolkata</button>
                    <button type="button" class="preset-city-btn" onclick="addPresetCity('Ahmedabad', 23.0225, 72.5714)">Ahmedabad</button>
                </div>

                <label>Custom Location</label>
                <div style="display: grid; grid-template-columns: 1.5fr 0.75fr 0.75fr 0.4fr; gap: 10px;">
                    <input type="text" id="customLocationName" placeholder="City/Location Name">
                    <input type="number" id="customLocationLat" placeholder="Latitude" step="0.0001" min="-90" max="90">
                    <input type="number" id="customLocationLon" placeholder="Longitude" step="0.0001" min="-180" max="180">
                    <button class="add-location-btn" type="button" onclick="addCustomLocation()" style="margin: 0; padding: 10px;">➕ Add</button>
                </div>

                <label style="margin-top: 15px;">Selected Locations</label>
                <div id="selectedLocations" class="locations-section">
                    <div style="color: #999; text-align: center; padding: 20px;">No locations selected. Click a city above or add a custom location.</div>
                </div>
            </div>

            <!-- Key Metrics -->
            <div class="card">
                <h2>📊 Key Metrics</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-value" id="totalDeliveries">10</div>
                        <div class="metric-label">Total Deliveries</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value" id="totalVehicles">3</div>
                        <div class="metric-label">Vehicles</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value" id="computeTime">0.00</div>
                        <div class="metric-label">Compute Time (ms)</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value" id="avgLoad">0%</div>
                        <div class="metric-label">Avg Load</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value" id="totalDistance">0.0</div>
                        <div class="metric-label">Total Distance (km)</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value" id="avgDistance">0.0</div>
                        <div class="metric-label">Avg/Vehicle (km)</div>
                    </div>
                </div>
            </div>

            <!-- Results Section -->
            <div class="card results-container">
                <h2>🎯 Algorithm Results</h2>

                <div class="tab-buttons">
                    <button class="tab-btn active" onclick="switchTab('overview')">Overview</button>
                    <button class="tab-btn" onclick="switchTab('fleet')">Fleet</button>
                    <button class="tab-btn" onclick="switchTab('deliveries')">Deliveries</button>
                </div>

                <!-- Overview Tab -->
                <div id="overview" class="tab-content active">
                    <div id="loading" class="loading">
                        <div class="spinner"></div>
                        <p>Optimizing routes...</p>
                    </div>

                    <div id="successMessage" class="success-message"></div>
                    <div id="errorMessage" class="error-message"></div>

                    <div id="algorithmResults" class="algorithm-results"></div>
                </div>

                <!-- Fleet Tab -->
                <div id="fleet" class="tab-content">
                    <div id="fleetSummary" class="fleet-summary"></div>
                </div>

                <!-- Deliveries Tab -->
                <div id="deliveries" class="tab-content">
                    <div class="comparison-table" id="deliveriesTable"></div>
                </div>
            </div>
        </div>

        <footer class="footer">
            <p>🎓 Design & Analysis of Algorithms (DAA) Mini Project | Version 2.0</p>
            <p>Production-Ready Delivery Optimization System</p>
        </footer>
    </div>

    <script>
        let currentResults = null;
        let selectedLocations = [];

        // Location Management Functions
        function renderLocations() {
            const container = document.getElementById('selectedLocations');
            if (selectedLocations.length === 0) {
                container.innerHTML = '<div style="color: #999; text-align: center; padding: 20px;">No locations selected. Click a city above or add a custom location.</div>';
                return;
            }
            container.innerHTML = selectedLocations.map((loc, idx) => `
                <div class="location-item">
                    <div><strong>${loc.name}</strong></div>
                    <div><small>Lat: ${loc.lat.toFixed(4)}</small></div>
                    <div><small>Lon: ${loc.lon.toFixed(4)}</small></div>
                    <button onclick="removeLocation(${idx})">❌</button>
                </div>
            `).join('');
        }

        function addPresetCity(name, lat, lon) {
            // Check if already added
            if (selectedLocations.some(l => l.name === name)) {
                alert(`${name} already added!`);
                return;
            }
            selectedLocations.push({ name, lat, lon });
            renderLocations();
        }

        function addCustomLocation() {
            const name = document.getElementById('customLocationName').value.trim();
            const lat = parseFloat(document.getElementById('customLocationLat').value);
            const lon = parseFloat(document.getElementById('customLocationLon').value);

            if (!name) {
                alert('Please enter a location name');
                return;
            }
            if (isNaN(lat) || lat < -90 || lat > 90) {
                alert('Invalid latitude. Must be between -90 and 90');
                return;
            }
            if (isNaN(lon) || lon < -180 || lon > 180) {
                alert('Invalid longitude. Must be between -180 and 180');
                return;
            }

            // Check if already added
            if (selectedLocations.some(l => l.name === name)) {
                alert(`${name} already added!`);
                return;
            }

            selectedLocations.push({ name, lat, lon });
            document.getElementById('customLocationName').value = '';
            document.getElementById('customLocationLat').value = '';
            document.getElementById('customLocationLon').value = '';
            renderLocations();
        }

        function removeLocation(index) {
            selectedLocations.splice(index, 1);
            renderLocations();
        }

        async function runOptimization() {
            const loading = document.getElementById('loading');
            const successMsg = document.getElementById('successMessage');
            const errorMsg = document.getElementById('errorMessage');
            
            loading.style.display = 'block';
            successMsg.style.display = 'none';
            errorMsg.style.display = 'none';

            try {
                const response = await fetch('/api/optimize', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        num_deliveries: parseInt(document.getElementById('numDeliveries').value),
                        num_vehicles: parseInt(document.getElementById('numVehicles').value),
                        depot_location: document.getElementById('depotLocation').value,
                        depot_lat: parseFloat(document.getElementById('depotLat').value),
                        depot_lon: parseFloat(document.getElementById('depotLon').value),
                        min_weight: parseFloat(document.getElementById('minWeight').value),
                        max_weight: parseFloat(document.getElementById('maxWeight').value),
                        min_capacity: parseFloat(document.getElementById('minCapacity').value),
                        max_capacity: parseFloat(document.getElementById('maxCapacity').value),
                        min_priority: parseInt(document.getElementById('minPriority').value),
                        max_priority: parseInt(document.getElementById('maxPriority').value),
                        custom_locations: selectedLocations
                    })
                });

                const data = await response.json();
                currentResults = data;

                if (data.error) {
                    errorMsg.textContent = '❌ ' + data.error;
                    errorMsg.style.display = 'block';
                } else {
                    successMsg.textContent = '✅ Optimization completed successfully!';
                    successMsg.style.display = 'block';

                    displayResults(data);
                }
            } catch (error) {
                errorMsg.textContent = '❌ Error: ' + error.message;
                errorMsg.style.display = 'block';
            } finally {
                loading.style.display = 'none';
            }
        }

        function displayResults(data) {
            // Update metrics
            document.getElementById('totalDeliveries').textContent = data.total_deliveries;
            document.getElementById('totalVehicles').textContent = data.total_vehicles;
            document.getElementById('computeTime').textContent = data.compute_time_ms.toFixed(2);
            document.getElementById('avgLoad').textContent = data.avg_load + '%';
            document.getElementById('totalDistance').textContent = data.route_metrics.total_distance_km.toFixed(1);
            document.getElementById('avgDistance').textContent = data.route_metrics.avg_distance_per_vehicle.toFixed(1);

            // Display algorithm results
            const resultsContainer = document.getElementById('algorithmResults');
            resultsContainer.innerHTML = '';

            const algorithms = data.summary;
            
            const algorithmOrder = [
                { key: 'activity_selection', name: 'Activity Selection', class: 'activity', type: 'Greedy' },
                { key: 'fractional_knapsack', name: 'Fractional Knapsack', class: 'knapsack', type: 'Greedy' },
                { key: 'max_priority_cluster', name: 'Max Sum Subarray', class: 'maxsum', type: 'DP' },
                { key: 'lcs_validation', name: 'LCS Matching', class: 'lcs', type: 'DP' }
            ];

            algorithmOrder.forEach(algo => {
                if (algorithms[algo.key]) {
                    const algoData = algorithms[algo.key];
                    const card = document.createElement('div');
                    card.className = `algorithm-card ${algo.class}`;
                    
                    let html = `
                        <div class="algorithm-name">${algo.name}</div>
                        <div class="algorithm-stat">
                            <span class="stat-label">Type:</span>
                            <span class="stat-value">${algo.type}</span>
                        </div>
                        <div class="algorithm-stat">
                            <span class="stat-label">Count:</span>
                            <span class="stat-value">${algoData.count}</span>
                        </div>
                    `;

                    if (algoData.total_weight) {
                        html += `
                            <div class="algorithm-stat">
                                <span class="stat-label">Weight:</span>
                                <span class="stat-value">${algoData.total_weight.toFixed(1)} kg</span>
                            </div>
                        `;
                    }

                    if (algoData.total_priority) {
                        html += `
                            <div class="algorithm-stat">
                                <span class="stat-label">Priority:</span>
                                <span class="stat-value">${algoData.total_priority}</span>
                            </div>
                        `;
                    }

                    card.innerHTML = html;
                    resultsContainer.appendChild(card);
                }
            });

            // Display fleet summary
            displayFleetSummary(data.vehicles);

            // Display deliveries
            displayDeliveries(data.deliveries);
        }

        function displayFleetSummary(vehicles) {
            const container = document.getElementById('fleetSummary');
            container.innerHTML = '<h3 style="color: #333; margin-bottom: 15px;">Vehicle Fleet</h3>';

            vehicles.forEach(vehicle => {
                const item = document.createElement('div');
                item.className = 'fleet-item';
                item.innerHTML = `
                    <div class="vehicle-name">🚐 ${vehicle.id} - ${vehicle.type}</div>
                    <div class="vehicle-stat">
                        <span>Capacity:</span>
                        <span>${vehicle.capacity_weight} kg</span>
                    </div>
                    <div class="vehicle-stat">
                        <span>Current Load:</span>
                        <span>${vehicle.current_load} kg (${vehicle.load_percentage}%)</span>
                    </div>
                    <div class="vehicle-stat">
                        <span>Deliveries:</span>
                        <span>${vehicle.route_size}</span>
                    </div>
                    <div class="vehicle-stat">
                        <span>Route Distance:</span>
                        <span>${vehicle.route_distance} km</span>
                    </div>
                `;
                container.appendChild(item);
            });
        }

        function displayDeliveries(deliveries) {
            const container = document.getElementById('deliveriesTable');
            let html = `
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Location</th>
                            <th>Priority</th>
                            <th>Weight (kg)</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            deliveries.forEach(d => {
                html += `
                    <tr>
                        <td><strong>${d.id}</strong></td>
                        <td>${d.address}</td>
                        <td><span class="metric-badge">${d.priority}</span></td>
                        <td>${d.weight.toFixed(1)}</td>
                        <td>${d.status}</td>
                    </tr>
                `;
            });

            html += `
                    </tbody>
                </table>
            `;
            container.innerHTML = html;
        }

        function switchTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('active');
            });

            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }

        function resetForm() {
            document.getElementById('numDeliveries').value = '8';
            document.getElementById('numVehicles').value = '3';
            document.getElementById('depotLocation').value = 'Mumbai Port, India';
            document.getElementById('depotLat').value = '19.0760';
            document.getElementById('depotLon').value = '72.8777';
            document.getElementById('minWeight').value = '20';
            document.getElementById('maxWeight').value = '150';
            document.getElementById('minCapacity').value = '300';
            document.getElementById('maxCapacity').value = '1200';
            document.getElementById('minPriority').value = '1';
            document.getElementById('maxPriority').value = '10';
            document.getElementById('successMessage').style.display = 'none';
            document.getElementById('errorMessage').style.display = 'none';
        }

        // Run optimization on page load
        window.addEventListener('load', runOptimization);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/optimize', methods=['POST'])
def optimize():
    try:
        data = request.json
        
        # Create custom depot
        depot = Location(
            id="depot_001",
            latitude=float(data.get('depot_lat', 19.0760)),
            longitude=float(data.get('depot_lon', 72.8777)),
            address=data.get('depot_location', 'Mumbai Port'),
            name="Main Depot"
        )

        # Get custom parameters from request
        num_deliveries = int(data.get('num_deliveries', 10))
        num_vehicles = int(data.get('num_vehicles', 3))
        min_weight = float(data.get('min_weight', 20))
        max_weight = float(data.get('max_weight', 150))
        min_capacity = float(data.get('min_capacity', 300))
        max_capacity = float(data.get('max_capacity', 1200))
        min_priority = int(data.get('min_priority', 1))
        max_priority = int(data.get('max_priority', 10))
        custom_locations = data.get('custom_locations', [])
        
        # Create sample data with custom parameters
        _, vehicles, all_deliveries = create_sample_data(
            num_vehicles=num_vehicles,
            min_weight=min_weight,
            max_weight=max_weight,
            min_capacity=min_capacity,
            max_capacity=max_capacity,
            min_priority=min_priority,
            max_priority=max_priority
        )
        
        # If custom locations provided, use them instead of random locations
        if custom_locations:
            deliveries = []
            for i, custom_loc in enumerate(custom_locations[:num_deliveries]):
                # Create delivery with custom location
                loc = Location(
                    id=f"LOC{i}",
                    latitude=custom_loc['lat'],
                    longitude=custom_loc['lon'],
                    address=custom_loc['name'],
                    name=custom_loc['name']
                )
                deliv = Delivery(
                    id=f"DEL-{2000+i}",
                    location=loc,
                    weight=all_deliveries[i].weight,  # Use generated weight
                    priority=all_deliveries[i].priority,  # Use generated priority
                    time_window=all_deliveries[i].time_window,
                    status=all_deliveries[i].status
                )
                deliveries.append(deliv)
        else:
            # Limit to requested number
            deliveries = all_deliveries[:num_deliveries]

        # Create optimizer
        optimizer = DeliveryOptimizer(depot)
        
        for vehicle in vehicles:
            optimizer.add_vehicle(vehicle)
        for delivery in deliveries:
            optimizer.add_delivery(delivery)

        # Run optimization
        results = optimizer.optimize_routes()

        # Calculate average load
        total_capacity = sum(v.capacity_weight for v in vehicles)
        total_load = sum(v.current_load_weight for v in vehicles)
        avg_load = int((total_load / total_capacity * 100)) if total_capacity > 0 else 0

        return jsonify({
            'success': True,
            'total_deliveries': len(deliveries),
            'total_vehicles': len(vehicles),
            'compute_time_ms': results['compute_time_ms'],
            'avg_load': avg_load,
            'route_metrics': {
                'total_distance_km': round(results['route_metrics']['total_distance_km'], 2),
                'avg_distance_per_vehicle': round(results['route_metrics']['average_distance_per_vehicle'], 2)
            },
            'summary': {
                'activity_selection': {
                    'count': results['summary']['activity_selection']['count'],
                    'type': 'Greedy'
                },
                'fractional_knapsack': {
                    'count': results['summary']['fractional_knapsack']['count'],
                    'total_weight': results['summary']['fractional_knapsack'].get('total_weight', 0),
                    'total_priority': results['summary']['fractional_knapsack'].get('total_priority', 0),
                    'type': 'Greedy'
                },
                'max_priority_cluster': {
                    'count': results['summary']['max_priority_cluster']['count'],
                    'total_priority': results['summary']['max_priority_cluster'].get('total_priority', 0),
                    'type': 'DP'
                },
                'lcs_validation': {
                    'count': 0,
                    'type': 'DP'
                }
            },
            'vehicles': [
                {
                    'id': v.id,
                    'type': v.vehicle_type.name,
                    'capacity_weight': round(v.capacity_weight, 1),
                    'current_load': round(v.current_load_weight, 1),
                    'load_percentage': round(v.get_load_percentage(), 1),
                    'route_size': len(v.route),
                    'route_distance': round(results['route_metrics']['vehicle_distances'].get(v.id, 0), 2)
                }
                for v in vehicles
            ],
            'deliveries': [
                {
                    'id': d.id,
                    'address': d.location.address,
                    'priority': d.priority,
                    'weight': round(d.weight, 1),
                    'status': d.status.value
                }
                for d in deliveries
            ]
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║  🚚 DELIVERY ROUTE OPTIMIZER - WEB APPLICATION          ║
    ║                                                          ║
    ║  Starting server...                                      ║
    ║  Open your browser and go to: http://localhost:8000     ║
    ║                                                          ║
    ║  Press Ctrl+C to stop the server                         ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    port = int(os.environ.get("PORT", 8000))
    app.run(debug=False, host='0.0.0.0', port=port)
