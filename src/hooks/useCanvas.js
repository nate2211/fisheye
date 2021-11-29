import {useState, useEffect, useRef} from 'react'
import axios from 'axios';
import {useMountedRef} from "./useMountedRef";
export function useCanvas(id){
    const mounted = useMountedRef();
    const [canvasPoints, setCanvas] = useState({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    console.log(id);
    useEffect(() => {
        if(!id) return;
        if(!mounted.current)return;
        axios.get(`http://127.0.0.1:8000/backend/search?author=${id}`).then(res => {if(!mounted.current) throw new Error("Component Not Mounted"); return res;})
            .then((res) => setCanvas(res.data))
            .then(() => setLoading(false))
            .catch((error) => {if(!mounted.current) return; setError(error)})
    }, [id]);
    return {canvasPoints, loading, error}

}
