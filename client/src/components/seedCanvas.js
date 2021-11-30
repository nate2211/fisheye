import React, {useRef, useEffect} from 'react';
import {Container, Canvas} from "react-bootstrap"

export default function SeedCanvas({data}){
    const canvasRef = useRef(null);
    useEffect(() => {
        const context = canvasRef.current.getContext('2d');



    }, [data]);
    return(<Container>
        <canvas ref={canvasRef} width="100" height="100"/>
    </Container>)
}