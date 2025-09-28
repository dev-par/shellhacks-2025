const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export class ApiClient {
  private baseUrl: string;
  private token: string | null = null;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  setToken(token: string | null) {
    this.token = token;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;

    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      ...(options.headers as Record<string, string>),
    };

    if (this.token) {
      headers.Authorization = `Bearer ${this.token}`;
    }

    const response = await fetch(url, {
      ...options,
      headers,
      credentials: "include", // Important for CORS with credentials
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.message || `HTTP error! status: ${response.status}`
      );
    }

    return response.json();
  }

  // Public endpoints (no auth required)
  async ping() {
    return this.request<{ status: string; message: string }>("/ping");
  }

  async health() {
    return this.request<{ status: string; service: string }>("/health");
  }

  // Auth endpoints (simplified for now)
  async getUser() {
    return this.request<{ status: string; user?: any }>("/auth/user");
  }

  // Protected endpoints (auth required)
  async getProtectedData() {
    return this.request<{ status: string; message: string; user?: any }>(
      "/api/protected"
    );
  }

  // Test connection without auth
  async testConnection() {
    try {
      const response = await fetch(`${this.baseUrl}/ping`);
      return await response.json();
    } catch (error) {
      throw new Error(`Connection failed: ${error}`);
    }
  }

  // Agent endpoints
  async sendMessage(
    message: string,
    agentType: string = "emergency_room_agent"
  ) {
    return this.request<{
      status: string;
      response: string;
      agent_type: string;
      agent_name: string;
    }>("/api/agent/message", {
      method: "POST",
      body: JSON.stringify({
        message,
        agent_type: agentType,
      }),
    });
  }

  // Group chat for training scenarios
  async sendGroupMessage(
    message: string,
    currentStage: number = 0,
    agentType: string = "emergency_room_agent"
  ) {
    return this.request<{
      status: string;
      response: string;
      agent_type: string;
      agent_name: string;
      current_stage: number;
    }>("/api/agent/group-chat", {
      method: "POST",
      body: JSON.stringify({
        message,
        current_stage: currentStage,
        agent_type: agentType,
        user_id: "default_user"
      }),
    });
  }

  async speechToText(audioData: string) {
    return this.request<{
      status: string;
      transcript: string;
      confidence: number;
    }>("/api/agent/speech-to-text", {
      method: "POST",
      body: JSON.stringify({ audio: audioData }),
    });
  }

  async textToSpeech(text: string) {
    return this.request<{ status: string; audio_url: string; text: string }>(
      "/api/agent/text-to-speech",
      {
        method: "POST",
        body: JSON.stringify({ text }),
      }
    );
  }
}

export const apiClient = new ApiClient();
