import React, {useState} from 'react'
import {Form, Container, Button} from "react-bootstrap"
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
        fdata.append('author', user.id);
        axios.post('http://127.0.0.1:8000/backend/canvas/', fdata).then((res) => {setData(res.data.canvasRectPoints); console.log(res)})
            .then(() => setRes((prev) => ({
                submit: true,
                c: prev.c + 1,
            }))).catch((error) => alert(error.message))
    };
    console.log('Upload Form Rerender');
    return(<Container className="uploadForm-cont">
        <Form onSubmit={(e) => onSubmit(e)}>
            <Form.Group>
                <Form.Label>Image</Form.Label>
                <Form.Control type="file" accept="image/*"  onChange={(e) => setImage(e.target.files[0])}/>
                {image !== null && <img src={URL.createObjectURL(image)} width="300" height="300" alt="preview"/>}
            </Form.Group>
            <Form.Group>
                <Button type="submit">Submit</Button>
            </Form.Group>
        </Form>
        {res.submit === true && <InputCanvas res={res} d={JSON.parse(data)}/>}
    </Container>)
}