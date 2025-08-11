import {
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  updateProfile,
} from "firebase/auth";
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { backend_Url } from "@/config";
import axios from "axios";

const firebaseConfig = {
  apiKey: "AIzaSyBVyvP7FdmBIw_NEhB3J835iTmLs_SAbN8",
  authDomain: "webscraper-af909.firebaseapp.com",
  projectId: "webscraper-af909",
  storageBucket: "webscraper-af909.firebasestorage.app",
  messagingSenderId: "481309650560",
  appId: "1:481309650560:web:cde81a8983439a8e928065",
  measurementId: "G-KZ5TKH7EGY",
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);

export async function login_e_p(email: string, password: string) {
  try {
    const userCred = await signInWithEmailAndPassword(auth, email, password);
    const token = await userCred.user.getIdToken();

    axios
      .post(backend_Url + "/login", { token }, { withCredentials: true })
      .then((response) => {
        if (response.status === 200) {
          console.log("Login sucessfull!", response.data.status);
        }
      })
      .catch((err) => {
        console.error("Login failed ", err.response?.status, err.message);
      });
  } catch (error: any) {
    console.error("err", error.code, error.message);
  }
}

export async function signup_e_p(
  email: string,
  password: string,
  firstname: string,
  lastname: string
) {
  try {
    const userCred = await createUserWithEmailAndPassword(
      auth,
      email,
      password
    );
    const user = userCred.user;
    await updateProfile(user, {
      displayName: `${firstname} ${lastname}`,
    });
    const token = await userCred.user.getIdToken();

    console.log({ token, userCred });

    axios
      .post(backend_Url + "/singup/", { token }, { withCredentials: true })
      .then((res) => {
        if (res.status === 200) {
          console.log("Singup sucessfull", res.data.status);
        }
      })
      .catch((err) => {
        console.error("Signup failed!", err.response?.status, err.message);
      });
  } catch (error: any) {
    console.error(
      "Signup failed",
      error.response?.status || error.code,
      error.message
    );
    return false;
  }
}

export async function check_User() {
  try {
    const res = await axios.get(`${backend_Url}/verify-auth/`, {
      withCredentials: true,
    });

    if (res.status === 200) {
      console.log("User is authenticated:", res.data.user);
      return res.data.user;
    }
  } catch (err: any) {
    console.warn("Not authenticated", err.response?.status);
    return null;
  }
}

export async function logout() {
  try {
    axios.get(backend_Url+'/logout/',{withCredentials:true})
    .then(res=>{console.log(res);})
    .catch(error=>{console.error("error :"+error);})
  } catch (error) {
    
  }
}