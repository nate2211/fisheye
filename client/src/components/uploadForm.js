import React, {useState} from 'react'
import {Form, Container, Button, Row, Col} from "react-bootstrap"
import "../styles/uploadform.css";
import axios from "axios";
import InputCanvas from "./inputCanvas";
import {useUser} from "../context/userContext";
export default function UploadForm() {
    const [image, setImage] = useState(null);
    const [res, setRes] = useState({submit: false, c: 0 });
    const [data, setData] = useState({});
    const {user} = useUser();
    const onSubmit = (e) => {
        e.preventDefault();
        var fdata = new FormData();
        fdata.append('Cimage', image);
        fdata.append('image_name', image.name);
        axios.post('https://natefsheye.herokuapp.com/backend/canvas/', fdata).then((res) => {setData(res.data.canvasRectPoints); console.log(res)})
            .then(() => setRes((prev) => ({
                submit: true,
                c: prev.c + 1,
            }))).catch((error) => alert(error.message))
    };
    console.log('Upload Form Rerender');
    return(<Container className="wrapper-cont">
        <Row>
            <Col>
        <Form onSubmit={(e) => onSubmit(e)} className="uploadForm-cont">
            <Form.Group>
                <Form.Label>Image</Form.Label>
                <Form.Control type="file" accept="image/*"  onChange={(e) => setImage(e.target.files[0])} style={{width: "50%"}}/>
                {image !== null && <img src={URL.createObjectURL(image)} width="300" height="300" alt="preview" style={{padding: "1rem"}}/>}
            </Form.Group>
            <Form.Group>
                <Button type="submit">Submit</Button>
            </Form.Group>
        </Form>
            </Col>
            <Col>
        {res.submit === true && <InputCanvas res={res} d={JSON.parse(data)} image={image}/>}
            </Col>
        </Row>
    </Container>)
}