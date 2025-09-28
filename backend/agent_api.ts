// Agent API client for ADK endpoints
const ADK_API_URL = 'http://127.0.0.1:8000'

export interface AgentMessage {
  role: 'user' | 'assistant';
  parts: Array<{ text: string }>;
}

export interface AgentResponse {
  events: Array<{
    id: string;
    author: string;
    content?: {
      parts: Array<{ text: string }>;
    };
    is_final_response?: boolean;
  }>;
}

export class AgentAPIClient {
  private appName = 'Emergensee';
  private userId: string;
  private sessionId: string | null = null;

  constructor(userId: string) {
    this.userId = userId;
  }

  // Create a new session
  async createSession(moduleId: string, scenarioId: number) {
    try {
      const response = await fetch(`${ADK_API_URL}/apps/${this.appName}/users/${this.userId}/sessions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          state: {
            states: {
              current_stage: 0,
              stages: ['S0_INITIAL_STABILIZATION', 'S1_DIAGNOSTIC_CONFIRMATION', 'S2_CRITICAL_CONSULTATION', 'S3_SENIOR_HANDOVER', 'S4_DEBRIEFING']
            },
            patient_information: this.getPatientInfo(moduleId, scenarioId),
            session_flags: {
              protocol_asa_given: false,
              protocol_ecg_ordered: false,
              protocol_diagnosis_confirmed: false,
              protocol_nitro_or_morphine: false
            },
            module_id: moduleId,
            scenario_id: scenarioId
          }
        })
      });

      if (!response.ok) {
        throw new Error('Failed to create session');
      }

      const data = await response.json();
      this.sessionId = data.session_id;
      return data;
    } catch (error) {
      console.error('Error creating session:', error);
      throw error;
    }
  }

  // Send message to agent
  async sendMessage(message: string): Promise<string> {
    if (!this.sessionId) {
      throw new Error('No active session');
    }

    try {
      const response = await fetch(`${ADK_API_URL}/run`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          app_name: this.appName,
          user_id: this.userId,
          session_id: this.sessionId,
          new_message: {
            role: 'user',
            parts: [{ text: message }]
          }
        })
      });

      if (!response.ok) {
        throw new Error('Failed to send message');
      }

      const data: AgentResponse = await response.json();
      
      // Extract the final response text
      let finalResponse = '';
      for (const event of data.events) {
        if (event.is_final_response && event.content?.parts) {
          for (const part of event.content.parts) {
            if (part.text) {
              finalResponse += part.text;
            }
          }
        }
      }

      return finalResponse || 'I received your message but need a moment to process it.';
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  }

  // Get session state
  async getSessionState() {
    if (!this.sessionId) {
      throw new Error('No active session');
    }

    try {
      const response = await fetch(`${ADK_API_URL}/apps/${this.appName}/users/${this.userId}/sessions/${this.sessionId}`);
      
      if (!response.ok) {
        throw new Error('Failed to get session state');
      }

      return await response.json();
    } catch (error) {
      console.error('Error getting session state:', error);
      throw error;
    }
  }

  // Get patient information based on scenario
  private getPatientInfo(moduleId: string, scenarioId: number) {
    if (moduleId === 'emergency-triage' && scenarioId === 1) {
      return {
        patient_name: "Sarah Johnson",
        patient_age: 34,
        static_patient_data: {
          vitals_snapshot: {
            BP_Systolic: 90,
            BP_Diastolic: 60,
            HR: 110,
            O2_Sat: 92,
            O2_Source: "Room Air",
            Pain_Score: 8
          },
          history: {
            Age_Sex: "34-year-old female",
            Complaint: "Motor vehicle accident with chest pain and difficulty breathing",
            Known_History: "Asthma, Previous appendectomy",
            Allergies: "Penicillin"
          }
        }
      };
    }
    
    // Default patient
    return {
      patient_name: "Brandon Hancock",
      patient_age: 55,
      static_patient_data: {
        vitals_snapshot: {
          BP_Systolic: 118,
          BP_Diastolic: 75,
          HR: 105,
          O2_Sat: 94,
          O2_Source: "Room Air",
          Pain_Score: 8
        },
        history: {
          Age_Sex: "55-year-old male",
          Complaint: "Crushing substernal chest pain",
          Known_History: "Hypertension, Smoker",
          Allergies: "None known"
        }
      }
    };
  }
}