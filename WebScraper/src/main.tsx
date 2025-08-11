import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Home from "./Page/Home.tsx";
import Layout from "./Page/Layout.tsx";
import { StorageContextProvider } from "./Storage/Storage.tsx";
import Account from "./Page/Account.tsx";
import Logout from "./Page/Logout.tsx";
import Chat from "./Page/Chat.tsx";
const route = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      {
        index: true,
        element: <Home />,
      },
      {
        path: "Home",
        element: <Home />,
      },
      {
        path: "Chat",
        element: <Chat />,
      },
      {
        path: "*",
        element: "Comming Soon",
      },
    ],
  },
  {
    path: "Account",
    element: <Account />,
  },
  {
    path: "/Logout",
    element: <Logout />,
  },
  {
    path: "*",
    element: "",
  },
]);
createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <StorageContextProvider>
      <RouterProvider router={route} />
    </StorageContextProvider>
  </StrictMode>
);
