import "bootstrap-icons/font/bootstrap-icons.css";
import "./../App.css";
import "./../index.css";

import { useStorage } from "@/Storage/Storage";
import { useForm, type SubmitHandler } from "react-hook-form";
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { loginUser, signupUser } from "@/Storage/BackendRequests";

type Inputs = {
  first_name: string;
  last_name: string;
  email: string;
  password: string;
};

export default function Account() {
  const { isDarkMode, setisAuth } = useStorage();
  const [Login, setLogin] = useState(false);
  const navigate = useNavigate();

  const toggleLogin = () => setLogin((prev) => !prev);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<Inputs>();

  const onSubmit: SubmitHandler<Inputs> = async (data) => {
    try {
      if (Login) {
        await loginUser({ email: data.email, password: data.password });
        setisAuth(true);
        navigate("/Home");
      } else {
        await signupUser({
          firstname: data.first_name,
          lastname: data.last_name,
          email: data.email,
          password: data.password,
        });
        setLogin(true);
      }
    } catch (error) {
      console.error(error);
      setisAuth(false);
    }
  };

  return (
    <div
      className={`min-h-screen flex items-center justify-center transition-colors duration-300 ${
        isDarkMode ? "bg-slate-900 text-white" : "bg-slate-100 text-slate-900"
      }`}
    >
      {/* Home Button */}
      <Link
        to="/Home"
        className="absolute top-6 left-6 p-3 rounded-full bg-blue-600 text-white shadow-lg hover:bg-blue-700 transition"
      >
        <i className="bi bi-house text-lg"></i>
      </Link>

      {/* Card */}
      <div
        className={`w-[360px] max-w-[92%] rounded-2xl shadow-xl p-6 ${
          isDarkMode ? "bg-slate-800" : "bg-white"
        }`}
      >
        {/* Toggle */}
        <div className="flex bg-slate-700 rounded-full p-1 mb-6">
          <button
            type="button"
            onClick={toggleLogin}
            className={`w-1/2 py-2 rounded-full text-sm font-semibold transition ${
              Login ? "bg-slate-600" : "bg-blue-600"
            }`}
          >
            Signup
          </button>
          <button
            type="button"
            onClick={toggleLogin}
            className={`w-1/2 py-2 rounded-full text-sm font-semibold transition ${
              Login ? "bg-blue-600" : "bg-slate-600"
            }`}
          >
            Login
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          {!Login && (
            <div className="flex gap-3">
              <div className="relative w-1/2">
                <i className="bi bi-person absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
                <input
                  {...register("first_name", { required: "First name required" })}
                  placeholder="First name"
                  className="w-full pl-10 py-3 rounded-full border focus:ring-2 focus:ring-blue-500 outline-none"
                />
              </div>

              <div className="relative w-1/2">
                <input
                  {...register("last_name", { required: "Last name required" })}
                  placeholder="Last name"
                  className="w-full pl-4 py-3 rounded-full border focus:ring-2 focus:ring-blue-500 outline-none"
                />
              </div>
            </div>
          )}

          {/* Email */}
          <div className="relative">
            <i className="bi bi-envelope absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
            <input
              {...register("email", {
                required: "Email is required",
                pattern: {
                  value: /^\S+@\S+$/i,
                  message: "Invalid email",
                },
              })}
              type="email"
              placeholder="Email"
              className="w-full pl-10 py-3 rounded-full border focus:ring-2 focus:ring-blue-500 outline-none"
            />
          </div>

          {/* Password */}
          <div className="relative">
            <i className="bi bi-lock absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
            <input
              {...register("password", {
                required: "Password required",
                minLength: {
                  value: 6,
                  message: "Minimum 6 characters",
                },
              })}
              type="password"
              placeholder="Password"
              className="w-full pl-10 py-3 rounded-full border focus:ring-2 focus:ring-blue-500 outline-none"
            />
          </div>

          {/* Errors */}
          {Object.values(errors).length > 0 && (
            <div className="text-red-500 text-sm space-y-1">
              {Object.values(errors).map((err, i) => (
                <p key={i}>{err?.message}</p>
              ))}
            </div>
          )}

          {/* Submit */}
          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 py-3 rounded-full font-semibold text-white transition"
          >
            {Login ? "Login" : "Create Account"}
          </button>
        </form>

        {/* Footer */}
        <div className="text-center mt-5 text-sm">
          {Login ? (
            <p>
              Don’t have an account?{" "}
              <button
                onClick={toggleLogin}
                type="button"
                className="text-blue-500 hover:underline"
              >
                Signup
              </button>
            </p>
          ) : (
            <p>
              Already have an account?{" "}
              <button
                onClick={toggleLogin}
                type="button"
                className="text-blue-500 hover:underline"
              >
                Login
              </button>
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
