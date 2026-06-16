const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const mqtt = require('mqtt');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

// Serve static files
app.use(express.static('public'));

// MQTT Connection
const MQTT_BROKER = 'mqtt://157.173.101.159';
const MQTT_TOPIC = 'HappyDavid';
const mqttClient = mqtt.connect(MQTT_BROKER);

let latestTemperature = '--';
let temperatureHistory = [];
const MAX_HISTORY = 50;

// Store connected WebSocket clients
const clients = new Set();

mqttClient.on('connect', () => {
    console.log('✅ Connected to MQTT Broker');
    mqttClient.subscribe(MQTT_TOPIC);
    console.log(`📤 Subscribed to topic: ${MQTT_TOPIC}`);
});

mqttClient.on('message', (topic, message) => {
    const tempValue = message.toString();
    console.log(`📥 Received: ${tempValue}°C`);
    
    latestTemperature = tempValue;
    
    // Add to history
    const timestamp = new Date();
    temperatureHistory.push({
        time: timestamp.toLocaleTimeString(),
        value: parseFloat(tempValue)
    });
    
    // Keep only last MAX_HISTORY entries
    if (temperatureHistory.length > MAX_HISTORY) {
        temperatureHistory.shift();
    }
    
    // Broadcast to all connected WebSocket clients
    const data = JSON.stringify({
        type: 'temperature',
        value: tempValue,
        timestamp: timestamp.toISOString(),
        history: temperatureHistory
    });
    
    clients.forEach(client => {
        if (client.readyState === WebSocket.OPEN) {
            client.send(data);
        }
    });
});

// WebSocket connection handling
wss.on('connection', (ws) => {
    console.log('🔗 Client connected to WebSocket');
    clients.add(ws);
    
    // Send current data immediately
    if (latestTemperature !== '--') {
        const data = JSON.stringify({
            type: 'temperature',
            value: latestTemperature,
            timestamp: new Date().toISOString(),
            history: temperatureHistory
        });
        ws.send(data);
    }
    
    ws.on('close', () => {
        console.log('🔌 Client disconnected');
        clients.delete(ws);
    });
});

// Serve dashboard
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/public/index.html');
});

// Start server on allowed port
const PORT = 9216; // Using one of your allowed ports
server.listen(PORT, '0.0.0.0', () => {
    console.log(`🚀 Dashboard running on http://0.0.0.0:${PORT}`);
    console.log(`📡 MQTT Topic: ${MQTT_TOPIC}`);
    console.log(`👥 Waiting for temperature data...`);
});