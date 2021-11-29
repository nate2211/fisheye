import React, {useState, createContext, useContext} from 'react'
const SeedContext = createContext();
export default function SeedProvider({children}){
    const[seeds, setSeeds] = useState([]);
    const addSeed = (element) => {
        setSeeds((prev) => [...prev, element])
    };
    const removeSeed = (element) => {
        setSeeds((prev) => prev.filter(e => e !== element))
    };

    const resetSeeds = () => {
        setSeeds(() => [])
    };
    return(<SeedContext.Provider value={{seeds, setSeeds, addSeed, removeSeed, resetSeeds}}>
        {children}
    </SeedContext.Provider>)
}

export const useSeeds = () => useContext(SeedContext);