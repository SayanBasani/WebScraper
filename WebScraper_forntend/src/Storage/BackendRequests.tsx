import api, { backend_Url } from "../config";

export async function isLogin() {
  // const response = await axios.get(backend_Url + "/status/", { withCredentials: true });
  const response = await api.get("/status/");
  // console.log(response);
  return response;
}

type LoginData = {
  username?: string;
  email: string;
  password: string;
};

type SignupData = {
  firstname: string;
  lastname: string;
  email: string;
  password: string;
};

export async function loginUser(data: LoginData) {
  try {
    if (!data.email || !data.password) {
      throw new Error("Email and password are required");
    }
    data.username = data.email; // Add username field for backend compatibility
    const response = await api.post("/login/", data);
    // console.log("Login response:");
    // console.log(response);
    const { access, refresh } = response.data;
    localStorage.setItem("access", access);
    localStorage.setItem("refresh", refresh);
    return response.data;
  } catch (error) {
    console.error("Error logging in:", error);
    throw error;
  }
}

export async function signupUser(data: SignupData) {
  try {
    const response = await api.post("/signup/", data);
    return response.data;
  } catch (error) {
    console.error("Error signing up:", error);
    throw error;
  }
}

export async function aiRequest(prompt: string) {
  try {
    const response = await api.post("/ai/request/", { p: prompt });
    return response.data;
  } catch (error) {
    console.error("Error making AI request:", error);
    throw error;
  }
}

export async function getSummery(URL: string) {
  try {
    const res: any = await api.post(
      // "/",
      "/ai/request/",
      // http://127.0.0.1:8000/ai/request/
      { q: URL },
      { withCredentials: true, headers: { "Content-Type": "application/json" } }
    );
    console.log(res);
    console.log(res.data);
    return res.data;
  } catch (error: any) {
    return { error: true, msg: error.response?.data || error.message };
  }
}

export async function getProfileData() {
  try {
    const response = await api.get("/profile/", {
      withCredentials: true,
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching profile data:", error);
    throw error;
  }
}

export async function downloadFile(
  info: {
    file_name: string;
    file_size: number;
    download_url: string;
  },
  onProgress?: (percent: number) => void
): Promise<{ videoUrl: string; blob: Blob }> {
  const response = await fetch(
    `${backend_Url}${info.download_url}?file=${encodeURIComponent(
      info.file_name
    )}`,
    {
      method: "GET",
      credentials: "include",
    }
  );

  if (!response.ok || !response.body) {
    throw new Error("Download failed");
  }

  const reader = response.body.getReader();
  const total = info.file_size;

  let received = 0;
  const chunks: Uint8Array[] = [];

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    chunks.push(value);
    received += value.length;

    if (onProgress) {
      onProgress(Math.floor((received / total) * 100));
    }
  }

  const blob = new Blob(chunks, { type: "video/mp4" });
  const videoUrl = URL.createObjectURL(blob);

  return { videoUrl, blob };
}
