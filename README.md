# Adaptive Emergency Response Training Simulator (AERTS)

A sophisticated medical simulation system designed for STEMI protocol training using a 5-state machine architecture with AI-powered agents and real-time voice interaction.

## Overview

AERTS provides an interactive, voice-driven emergency room drill system that simulates a complete STEMI (ST-Elevation Myocardial Infarction) case from initial presentation to senior handover. The system uses multiple AI agents to create realistic training scenarios with dynamic responses and comprehensive evaluation.

## Key Features

### 5-State Machine Architecture
- **S1: INITIAL_STABILIZATION** - Gather history, secure IV access, administer aspirin
- **S2: DIAGNOSTIC_CONFIRMATION** - ECG completion, pain management, vital monitoring
- **S3: CRITICAL_CONSULTATION** - SBAR consultation with remote Doctor Agent
- **S4: SENIOR_HANDOVER** - Structured handover to Senior Doctor
- **S5: DEBRIEFING** - Final evaluation and performance feedback

### AI Agent System
- **Coordinator Agent**: Manages state transitions and validates commands
- **Nurse Agent**: Uses Gemini LLM for dynamic dialogue responses
- **Doctor Agent**: Handles SBAR consultation and Senior Doctor handover
- **Evaluator Agent**: Provides comprehensive performance assessment

### Clinical Safety Features
- Real-time clinical gate checks for contraindications
- Automatic safety warnings for inappropriate orders
- Medication interaction validation
- Vital sign monitoring and alerts

### Voice Integration
- Speech-to-text for natural command input
- Text-to-speech for agent responses
- Medical terminology validation
- Multi-agent voice differentiation

## Architecture

### Backend (Python/FastAPI)
```
backend/
├── main.py                 # FastAPI application and endpoints
├── agents/                 # AI agent implementations
│   ├── coordinator.py     # 5-state machine coordinator
│   ├── nurse.py          # Gemini-powered nurse agent
│   ├── doctor.py         # SBAR and handover specialist
│   └── evaluator.py      # Performance evaluation
├── models/                # Data models and schemas
│   ├── scenario.py       # AERTS state and patient models
│   └── commands.py       # Command and response models
├── services/              # External service integrations
│   ├── gemini_service.py # Google Gemini AI integration
│   ├── a2a_client.py     # Agent-to-Agent communication
│   └── voice_service.py  # Speech processing
└── requirements.txt       # Python dependencies
```

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+ (for future frontend)
- Google Cloud API key (optional, for Gemini integration)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd shellhacks-2025
```

2. **Set up the backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure environment (optional)**
```bash
cp env.example .env
# Edit .env with your Google Cloud API key
```

4. **Run the backend**
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### API Documentation
- Interactive API docs: `http://localhost:8000/docs`
- OpenAPI schema: `http://localhost:8000/openapi.json`

## Usage

### Starting a Simulation

```bash
curl -X POST "http://localhost:8000/api/session/start" \
     -H "Content-Type: application/json"
```

Response:
```json
{
  "session_id": "uuid-here",
  "current_state": "S1_INITIAL_STABILIZATION",
  "patient": {
    "age": 55,
    "gender": "male",
    "chief_complaint": "crushing substernal chest pain",
    "pain_level": 8,
    "vitals": {
      "bp": "140/90",
      "hr": 95,
      "rr": 18,
      "temp": 98.6,
      "o2_sat": 96
    }
  }
}
```

### Processing Commands

```bash
curl -X POST "http://localhost:8000/api/session/{session_id}/command" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Give aspirin 325mg",
       "timestamp": "2024-01-01T12:00:00Z",
       "command_type": "order"
     }'
```

### SBAR Consultation Tool

```bash
curl -X POST "http://localhost:8000/api/session/{session_id}/tool/sbar_consult" \
     -H "Content-Type: application/json" \
     -d '{
       "situation": "55-year-old male with chest pain",
       "background": "No known cardiac history",
       "assessment": "High suspicion for STEMI",
       "recommendation": "Continue current management"
     }'
```

### Senior Handover Tool

```bash
curl -X POST "http://localhost:8000/api/session/{session_id}/tool/handover" \
     -H "Content-Type: application/json" \
     -d '{
       "patient_summary": "55-year-old male with STEMI",
       "current_status": "Stable on current interventions",
       "interventions_performed": ["Aspirin", "ECG", "IV access"],
       "pending_actions": ["Cardiology consult"],
       "critical_concerns": ["Ongoing chest pain"]
     }'
```

## State Machine Details

### S1: INITIAL_STABILIZATION
**Goal**: Gather history and secure initial access
**Key Actions**:
- Administer aspirin 325mg
- Order 12-lead ECG
- Establish IV access
- Start oxygen if needed

**Transition Triggers**:
- Aspirin administered AND ECG ordered → S2

### S2: DIAGNOSTIC_CONFIRMATION
**Goal**: Complete diagnostic workup and pain management
**Key Actions**:
- ECG results (automatic after 5 seconds)
- Order nitroglycerin (if BP > 100)
- Order morphine for pain
- Monitor vitals

**Transition Triggers**:
- ECG completed → S3

### S3: CRITICAL_CONSULTATION
**Goal**: SBAR consultation with Doctor Agent
**Key Actions**:
- Use SBAR tool for consultation
- Receive approval/feedback
- Prepare for handover

**Transition Triggers**:
- SBAR approved → S4

### S4: SENIOR_HANDOVER
**Goal**: Structured handover to Senior Doctor
**Key Actions**:
- Use handover tool
- Present comprehensive case summary
- Receive evaluation

**Transition Triggers**:
- Handover completed → S5

### S5: DEBRIEFING
**Goal**: Final evaluation and feedback
**Key Actions**:
- Generate final debrief
- Calculate performance scores
- Provide recommendations

## Agent Interactions

### Coordinator Agent
- Manages the 5-state machine
- Validates all commands
- Enforces clinical safety rules
- Publishes intents to other agents

### Nurse Agent (Gemini-Powered)
- Responds dynamically to coordinator intents
- Provides realistic clinical updates
- Executes orders and reports results
- Uses medical terminology appropriately

### Doctor Agent
- Handles SBAR consultation requests
- Evaluates SBAR quality and provides feedback
- Acts as Senior Doctor for handover
- Provides clinical guidance and approval

### Evaluator Agent
- Tracks performance throughout simulation
- Calculates comprehensive scores
- Generates detailed feedback
- Identifies areas for improvement

## Clinical Safety Features

### Safety Gate Checks
- **Nitroglycerin**: Checks systolic BP > 100 mmHg
- **Morphine**: Monitors respiratory rate > 12/min
- **Oxygen**: Validates O2 saturation requirements
- **IV Medications**: Ensures IV access established

### Warning System
- Real-time contraindication alerts
- Alternative medication suggestions
- Safety recommendations
- Clinical reasoning prompts

## Scoring System

### Evaluation Criteria
- **SBAR Completeness** (25%): Structure and content quality
- **Clinical Accuracy** (25%): Appropriate interventions
- **Communication Quality** (20%): Clarity and professionalism
- **Timing Efficiency** (15%): Protocol adherence timing
- **Safety Awareness** (15%): Contraindication recognition

### Performance Levels
- **Expert** (90-100): Outstanding performance
- **Advanced** (80-89): Very good with minor improvements
- **Intermediate** (70-79): Good with several areas to address
- **Novice** (<70): Needs significant improvement

## Configuration

### Environment Variables
```bash
# Google Cloud Configuration (optional)
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account-key.json

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Logging
LOG_LEVEL=INFO
DEBUG=True
```

### Gemini Integration
To enable Gemini AI responses:
1. Get a Google Cloud API key
2. Set `GOOGLE_APPLICATION_CREDENTIALS` environment variable
3. Install Google Generative AI: `pip install google-generativeai`

Without Gemini, the system uses intelligent mock responses.

## Development

### Adding New States
1. Update state machine in `coordinator.py`
2. Add transition logic
3. Update agent response handling
4. Add tests for new state

### Adding New Agents
1. Create agent class in `agents/`
2. Implement required methods
3. Register in `main.py`
4. Add voice configuration

### Customizing Scoring
1. Modify criteria in `evaluator.py`
2. Update weights and thresholds
3. Add new evaluation metrics
4. Test with sample scenarios

## API Endpoints

### Session Management
- `POST /api/session/start` - Start new simulation
- `GET /api/session/{id}/status` - Get session status
- `POST /api/session/{id}/end` - End simulation

### Command Processing
- `POST /api/session/{id}/command` - Process trainee command
- `POST /api/session/{id}/tool/sbar_consult` - SBAR consultation
- `POST /api/session/{id}/tool/handover` - Senior handover

### WebSocket
- `WS /ws/{session_id}` - Real-time voice communication

## Testing

### Manual Testing
1. Start the backend server
2. Use the API documentation at `/docs`
3. Test each state transition
4. Verify agent responses
5. Check scoring accuracy

### Automated Testing
```bash
# Run tests (when implemented)
pytest tests/
```

## Troubleshooting

### Common Issues
1. **Gemini not working**: Check API key and internet connection
2. **Voice not working**: Verify Google Cloud Speech API setup
3. **State not transitioning**: Check command format and timing
4. **Agent not responding**: Verify agent initialization

### Logs
Check application logs for detailed error information:
```bash
tail -f logs/aerts.log
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Cloud Speech-to-Text and Text-to-Speech APIs
- Google Gemini AI for dynamic responses
- FastAPI and Python communities
- Medical education professionals for clinical guidance
