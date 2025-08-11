import "bootstrap-icons/font/bootstrap-icons.css";
import "./../App.css";
import "./../index.css";
import { useStorage } from "@/Storage/Storage";
import { useForm, type SubmitHandler } from "react-hook-form";
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { login_e_p, signup_e_p } from "@/Component/firebase";

type Inputs = {
  firstname: string;
  lastname: string;
  email: string;
  password: string;
};

export default function Account() {
  const { isDarkMode, setisAuth } = useStorage();
  const [Login, setLogin] = useState(false);
  const [LSmessage, setLSMessage] = useState({});
  const navigate = useNavigate();
  const toggleLogin = () => {
    setLogin((prev) => !prev);
  };
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<Inputs>();
  console.log(LSmessage);
  const onSubmit: SubmitHandler<Inputs> = async (data) => {
    console.log("Form data:", data);
    try {
      if (data.email || data.password) {
        if (Login) {
          // it is for Login
          await login_e_p(data.email, data.password);
          setLSMessage({ login: true });
          navigate("/Home");
          setisAuth(true);
        } else {
          await signup_e_p(data.email, data.password,data.firstname , data.lastname);
          setLSMessage({ login: true });
          setisAuth(true);
        }
      }
    } catch (error: any) {
      setisAuth(false);
      setLSMessage({ login: false, msg: error.message });
    }
  };

  return (
    <div
      className={`h-screen ${
        isDarkMode ? "bg-gray-900 text-white" : "bg-white text-black"
      }`}>
        <Link to={'/Home'} className=""><i className="bi bi-house"></i></Link>
      <div className="w-full h-full flex justify-center items-center">
        <div className="w-full flex justify-center items-center h-full">
          <div className="pt-4 p-6 bg-gray-700 text-white rounded-md shadow w-[320px] py-16 transition-transform delay-300 ease-in-out">
            <div className="my-3 flex justify-center p-2 gap-[1px]">
              <button
                onClick={toggleLogin}
                className={`rounded-l-2xl px-3 justify-end py-1 hover:bg-blue-400 ${
                  Login ? "bg-gray-600" : "bg-blue-600"
                }`}
                type="button">
                SingUp
              </button>
              <button
                onClick={toggleLogin}
                className={`rounded-r-2xl px-3 justify-start py-1 hover:bg-blue-400 ${
                  Login ? "bg-blue-600" : "bg-gray-600"
                }`}
                type="button">
                Login
              </button>
            </div>
            <form
              onSubmit={handleSubmit(onSubmit)}
              className="flex flex-col gap-3">
              {Login ? (
                ""
              ) : (
                <div className={`flex w-full justify-between`}>
                  <div className={`w-[45%]`}>
                    <input
                      {...register("firstname", {
                        required: "Username is required",
                      })}
                      type="text"
                      placeholder="Fullname"
                      className="border p-2 rounded-3xl w-full"
                    />
                    {errors.firstname && (
                      <span className="text-red-500 text-sm">
                        {errors.firstname.message}
                      </span>
                    )}
                  </div>
                  <div className={`w-[45%]`}>
                    <input
                      {...register("lastname", {
                        required: "Lastname is required",
                      })}
                      type="text"
                      placeholder="Lastname"
                      className="border p-2 rounded-3xl w-full"
                    />
                    {errors.lastname && (
                      <span className="text-red-500 text-sm">
                        {errors.lastname.message}
                      </span>
                    )}
                  </div>
                </div>
              )}

              <input
                {...register("email", {
                  required: "Email is required",
                  pattern: {
                    value: /^\S+@\S+$/i,
                    message: "Invalid email address",
                  },
                })}
                type="email"
                placeholder="Email"
                className="border p-2 rounded-3xl"
              />
              {errors.email && (
                <span className="text-red-500 text-sm">
                  {errors.email.message}
                </span>
              )}

              <input
                {...register("password", {
                  required: "Password is required",
                  minLength: {
                    value: 6,
                    message: "Minimum 6 characters required",
                  },
                })}
                type="password"
                placeholder="Password"
                className="border p-2 rounded-3xl"
              />
              {errors.password && (
                <span className="text-red-500 text-sm">
                  {errors.password.message}
                </span>
              )}

              <button
                type="submit"
                className="bg-blue-600 hover:bg-blue-700 text-white py-2 rounded mt-2">
                Submit
              </button>
            </form>
            <div className="my-3">
              {Login ? (
                <>
                  <p>
                    Alredy have an Account.{" "}
                    <span className="text-blue-400 hover:underline">
                      <button onClick={toggleLogin} type="button">Login</button>
                    </span>
                  </p>
                </>
              ) : (
                <>
                  <p>
                    I dont't have an Account.{" "}
                    <span className="text-blue-400 hover:underline">
                      <button onClick={toggleLogin} type="button">Signup</button>
                    </span>
                  </p>
                </>
              )}
            </div>
          </div>
        </div>

        {/* <div className="overflow-hidden w-full h-full grid grid-cols-1 max-sm:hidden sm:grid-cols-2 lg:grid-cols-4 xl:grid-cols-5 place-items-center"> */}
        <div className="hidden overflow-hidden w-full h-full  grid-cols-1 max-sm:hidden sm:grid-cols-2 lg:grid-cols-4 xl:grid-cols-5 place-items-center">
          <div className="div particle"></div>
          <div className="div cells"></div>
          <div className="div jelly"></div>
          <div className="div blobbs"></div>
          <div className="div chase"></div>
        </div>
      </div>
    </div>
  );
}
