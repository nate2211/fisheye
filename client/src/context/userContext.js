import React, {useState, createContext, useContext} from 'react'
import axios from "axios";
const UserContext = createContext();

export default function UserProvider({children}) {
    const [user, setUser] = useState(JSON.parse(window.localStorage.getItem('user')) || null);

    const UserSet = async (obj) => {
        console.log(obj);
        window.localStorage.setItem('user', JSON.stringify(obj));
        setUser(obj)
    };
    const SignOut = () =>  {
        window.localStorage.clear();
        setUser(null)
    };

    return(<UserContext.Provider value={{UserSet, user, SignOut}}>
        {children}
    </UserContext.Provider>)

}

export const useUser = () => useContext(UserContext);