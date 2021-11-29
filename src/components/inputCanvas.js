import React, {useEffect, useRef, useState} from 'react'
import "../styles/canvas.css";
import {ListGroup, Button, Form} from "react-bootstrap";
import {useSeeds} from "../context/seedContext";
import axios from 'axios'
export default function InputCanvas({res, d}){
    // eslint-disable-next-line no-undef
    const canvasRef = useRef();

    const [scale] = useState(5);
    const {seeds, setSeeds, addSeed, removeSeed, resetSeeds} = useSeeds();
    function drawGrid(){
        const context = canvasRef.current.getContext('2d');
        for(let y = 0; y < canvasRef.current.width / scale; y++){
            for(let x =0; x < canvasRef.current.height / scale; x++){
                context.rect(x * scale, y*scale, scale, scale);

                let current = d[`(${x}, ${y})`];
                current = current.split(" ");
                context.fillStyle = `rgb(${current[0]},${current[1]},${current[2]})`;
                context.fillRect(x * scale, y * scale, scale, scale);
                context.strokeRect(x*scale, y*scale, scale, scale);
            }
        }
    }
    function canvasClick(e){
        let x = e.offsetX;
        let y = e.offsetY;
        x = Math.round(x / scale);
        y = Math.round(y / scale);
        console.log(x, y);
        let current = d[`(${x}, ${y})`];
        current = current.split(" ");
        console.log(current);
        addSeed([x, y, `rgb(${current[0]},${current[1]},${current[2]})`])

    }

    const onSubmit = (e) => {
        e.preventDefault();
        let data = new FormData()
        data.append('canvas')
        data.append('file', );
        axios.post('http://127.0.0.1:8000/backend/images/', data)


    }
    useEffect(() => {
        const canvas = canvasRef.current;
        drawGrid();
        const listen = function(e){
            canvasClick(e)
        }
        canvas.addEventListener('mousedown', listen);
        resetSeeds();
        return () => {
            canvas.removeEventListener('mousedown', listen)
        }

    }, [res.c]);


    return(<div className="canvas-cont">
        <canvas ref={canvasRef} width="500" height="500"/>
        <SeedPoints seeds={seeds} removeSeed={removeSeed}/>
        {seeds.length > 1 && <RegionColor seeds={seeds}/>}
        {seeds.length > 1 && <Button onClick={(e) => onSubmit(e)}>Submit</Button>}
    </div>)
}

const SeedPoints = ({seeds, removeSeed}) => {
    return(
        <div className="seedpoints-list">
            <h5>Seed Points</h5>
            <ListGroup>
        {seeds.map((seed, k) => {return <ListGroup.Item key={k}><SeedPoint seed={seed}  removeSeed={removeSeed}/></ListGroup.Item>})}

    </ListGroup></div>)
};
const SeedPoint = ({seed,  removeSeed = f => f}) => {
    return(<div>
        <h5>{seed[0]}, {seed[1]}</h5>
        <div style={{backgroundColor: seed[2], width: 50, height: 50}}/>
        <button onClick={() => removeSeed(seed)}>Remove</button>
    </div>)

};

const RegionColor = ({seed}) =>{


    return(<Form>
        {seed.map((seed, o) => {return(<Form.Group key={o}>
            <Form.Control type={"color"}/>
        </Form.Group>)} )}
    </Form>)
}