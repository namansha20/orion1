# ORION-EYE Quick Start Guide

## 5-Minute Setup

### Step 1: Install (1 minute)
```bash
git clone https://github.com/namansha20/orion.git
cd orion
pip install -r requirements.txt
```

### Step 2: Run (1 minute)
```bash
python app.py
```

### Step 3: Open Browser (1 minute)
Navigate to: **http://localhost:5000**

### Step 4: Test Demos (2 minutes)
Click the three demo buttons:
1. **Demo 1: Safe Passage** - See nominal operations
2. **Demo 2: Collision Course** - Watch autonomous avoidance
3. **Demo 3: Multiple Objects** - Experience complex decision-making

## What You'll See

### Dashboard Features
- **System Status**: Real-time object counts and risk levels
- **3D Visualization**: Spacecraft (blue) and objects (color-coded by risk)
- **Decision Box**: Autonomous AI decision with reasoning
- **Object Table**: All detected objects with risk assessment
- **Maneuver Planning**: Delta-V, fuel cost, and success probability
- **XAI Logs**: Complete decision trail with timestamps
- **LEO Impact**: Environmental impact analysis

### Risk Color Coding
- 🟢 **Green**: LOW risk - safe distance
- 🟡 **Yellow**: MEDIUM risk - monitor
- 🟠 **Orange**: HIGH risk - maneuver required
- 🔴 **Red**: CRITICAL risk - immediate action

## Command Line Demos

### Test Core System
```bash
python orion_eye.py
```
Outputs JSON result of safe scenario simulation.

### Run Test Suite
```bash
python test_demos.py
```
Validates all 10 layers across 3 scenarios.

### XAI Demonstration
```bash
python demo_xai.py
```
Shows explainable AI decision logs for all scenarios.

## API Usage

### Health Check
```bash
curl http://localhost:5000/api/health
```

### Get Scenarios
```bash
curl http://localhost:5000/api/scenarios
```

### Run Simulation
```bash
curl -X POST http://localhost:5000/api/simulate \
  -H "Content-Type: application/json" \
  -d '{"scenario":"crash"}'
```

## Troubleshooting

### Port Already in Use
If port 5000 is busy:
```bash
# Edit app.py and change port to 8000
app.run(debug=debug_mode, host='0.0.0.0', port=8000)
```

### Module Not Found
```bash
# Ensure all dependencies installed
pip install --upgrade -r requirements.txt
```

### Browser Not Loading
- Check firewall settings
- Try: http://127.0.0.1:5000
- Use Chrome or Firefox (recommended)

## Production Deployment

### Enable Debug Mode (Development Only)
```bash
export FLASK_ENV=development
python app.py
```

### Disable Debug Mode (Production - Default)
```bash
python app.py
# Debug mode is off by default for security
```

### Use Production Server
For production deployment, use a WSGI server:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Next Steps

1. **Explore**: Try all three demos
2. **Customize**: Modify scenarios in `orion_eye.py`
3. **Extend**: Add new layers or ML models
4. **Integrate**: Connect to real sensors or spacecraft systems
5. **Present**: Use for hackathon or demonstration

## Key Files

- `app.py` - Web server
- `orion_eye.py` - Core AI system (10 layers)
- `templates/index.html` - Dashboard UI
- `test_demos.py` - Validation tests
- `demo_xai.py` - XAI demonstration
- `README.md` - Full documentation
- `LOGIC_FLOW.md` - Algorithm details
- `IMPLEMENTATION_GUIDE.md` - Hackathon strategy

## Support

For issues or questions:
1. Check README.md for detailed documentation
2. Review LOGIC_FLOW.md for algorithm understanding
3. See IMPLEMENTATION_GUIDE.md for presentation tips

---

**Ready in 5 minutes. Autonomous in milliseconds.** 🚀
