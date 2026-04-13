import React, {
  createContext,
  useContext,
  useState,
  type ReactNode,
  type SetStateAction,
} from "react";

interface storageProviderProp {
  children: ReactNode;
}

const StorageContext = createContext<storageContextProp | undefined>(undefined);

interface storageContextProp {
  isAuth: boolean;
  setisAuth: React.Dispatch<SetStateAction<boolean>>;
  isDarkMode: boolean;
  setisDarkMode: React.Dispatch<SetStateAction<boolean>>;
  chatmsg: any;
  setchatmsg: React.Dispatch<SetStateAction<any>>;
  isLoading: boolean;
  setIsLoading: React.Dispatch<SetStateAction<boolean>>;
}

export function StorageContextProvider({ children }: storageProviderProp) {
  const [isAuth, setisAuth] = useState(true);
  const [isDarkMode, setisDarkMode] = useState(true);
  const [chatmsg, setchatmsg] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  
  return (
    <StorageContext.Provider
      value={{
        isAuth,
        setisAuth,
        isDarkMode,
        setisDarkMode,
        chatmsg,
        setchatmsg,
        isLoading,
        setIsLoading,
      }}>
      {children}
    </StorageContext.Provider>
  );
}

export function useStorage() {
  const context = useContext(StorageContext);
  if (context === undefined) {
    throw new Error("storage contect undefined");
  }
  return context;
}
