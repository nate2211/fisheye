import React, {useEffect, useRef, useState} from 'react'
import "../styles/canvas.css";
import {ListGroup, Button, Form, Container, Col} from "react-bootstrap";
import {useSeeds} from "../context/seedContext";
import axios from 'axios'
export default function InputCanvas({res, d, image}){
    // eslint-disable-next-line no-undef
    const canvasRef = useRef();
    const thresRef = useRef();
    const [scale] = useState(10);
    const [data, setData] = useState(null);
    const [op, setOp] = useState(true)
    const {seeds, setSeeds, addSeed, removeSeed, resetSeeds, points} = useSeeds();
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
        let ex = e.offsetX;
        let ey = e.offsetY;
        let x = Math.round(ex / scale);
        let y = Math.round(ey / scale);
        let current = d[`(${x}, ${y})`];
        current = current.split(" ")
        addSeed([x, y, `rgb(${current[0]},${current[1]},${current[2]})`], [`(${Math.round(x * 3)},${Math.round(y * 3)})`])

    }

    const onSubmit = (e) => {
        e.preventDefault();
        let data = new FormData()
        data.append('image_name', image.name)
        data.append('outputImage', image);
        data.append('t', thresRef.current.value)
        data.append('points', JSON.stringify(points))
        data.append('op', op)
        axios.post('http://127.0.0.1:8000/backend/images/', data).then((res) => setData(res.data))
            .catch((error) => alert(error.message))


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


    return(<Container>
        <Col>
        <canvas ref={canvasRef} width="1000" height="1000"/>
        </Col>
        <Col className="seedpoints-list">
        <SeedPoints seeds={seeds} removeSeed={removeSeed} scale={scale}/>
        </Col>
        <Form.Group className="p-2">
            <Form.Label>Thrs</Form.Label>
            <Form.Control type="number" ref={thresRef}/>
        </Form.Group>
        <Form.Group className="p-2">
            <Form.Label>Closing</Form.Label>
            <Form.Check  onClick={(e) => setOp(!e.target.checked)}/>
        </Form.Group>
        <Form.Group>
            {seeds.length !== 0 && <Button onClick={(e) => onSubmit(e)}>Submit</Button>}
        </Form.Group>
        {data !== null && <img src={data.outputImage} style={{width: 800, height: 600}} alt="output"/>}
    </Container>)
}

const SeedPoints = ({seeds, removeSeed, scale}) => {
    return(
        <div className="seedpoints-list">
            <h5>Seed Points</h5>
            <ListGroup>
        {seeds.map((seed, k) => {return <ListGroup.Item key={k}><SeedPoint seed={seed}  removeSeed={removeSeed} scale={scale}/></ListGroup.Item>})}

    </ListGroup></div>)
};
const SeedPoint = ({seed,  removeSeed = f => f, scale}) => {
    return(<div>
        <h5>{seed[0] * scale}, {seed[1] * scale}</h5>
        <div style={{backgroundColor: seed[2], width: 50, height: 50}}/>
        <button onClick={() => removeSeed(seed, [`(${seed[1]},${seed[0]})`])}>Remove</button>
    </div>)

};

const RegionColor = ({seed}) =>{
    const colorRef = useRef(null)

    return(<Form>
        <Form.Group>
            <Form.Control type={"color"} ref={colorRef}/>
        </Form.Group>
    </Form>)
}