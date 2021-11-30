import React, {useState, createContext, useContext} from 'react'
const SeedContext = createContext();
export default function SeedProvider({children}){
    const[seeds, setSeeds] = useState([]);
    const [points, setPoints] = useState([])
    const addSeed = (element, point) => {
        setSeeds((prev) => [...prev, element])
        setPoints((prev) => [...prev, point])
    };
    const removeSeed = (element, point) => {
        setSeeds((prev) => prev.filter(e => e !== element))
        setPoints((prev) => prev.filter(e => e !== point))
    };
    const resetSeeds = () => {
        setSeeds(() => [])
        setPoints(() => [])
    };
    return(<SeedContext.Provider value={{seeds, setSeeds, addSeed, removeSeed, resetSeeds, points}}>
        {children}
    </SeedContext.Provider>)
}

export const useSeeds = () => useContext(SeedContext);