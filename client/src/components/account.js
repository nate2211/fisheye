import React, {useEffect, useRef, useState} from 'react';
import {Form, Button, Container} from "react-bootstrap"
import * as RoutesE from "../routes";
import {Link} from "react-router-dom"
import axios from "axios";
import {useUser} from "../context/userContext";
import { useNavigate } from "react-router-dom";
import {ErrorScreen} from "./errorBoundary";

export const SignIn = () => {
    const email = useRef(null);
    const username = useRef(null);
    const password = useRef(null);
    const {UserSet} = useUser();
    const navigate = useNavigate();
    const onSubmit = (e) => {
        e.preventDefault();
        let data = new FormData();
        data.append('email', email.current.value);
        data.append("username", username.current.value);
        data.append("password", password.current.value);
        axios.post("http://127.0.0.1:8000/rest-auth/login/", data)
            .then((res) => UserSet({username: username.current.value, email: email.current.value, token: res.data.key, id: res.data.user}))
            .then(() => navigate("/") )
            .catch((error) => alert(error.message))

    };
    return(<Form onSubmit={(e) => onSubmit(e)}>
        <h2>Sign In</h2>
        <Form.Group>
            <Form.Label>Email</Form.Label>
            <Form.Control type="email" ref={email}/>
        </Form.Group>
        <Form.Group>
            <Form.Label>UserName</Form.Label>
            <Form.Control type="text" ref={username}/>
        </Form.Group>
        <Form.Group>
            <Form.Label>Password</Form.Label>
            <Form.Control type="password" ref={password}/>
        </Form.Group>
        <Button type="submit">Submit</Button>
        <span><Link to={RoutesE.signup}>No Account? Sign Up!</Link></span>
        <span><Link to={RoutesE.forget}>Forget Password?</Link></span>
    </Form>)
};

export const SignUp = () => {

    const username = useRef(null);
    const password = useRef(null);
    const password2 = useRef(null);
    const email = useRef(null);

    const onSubmit = (e) => {
        e.preventDefault();
        let data = new FormData();
        data.append("email", email.current.value);
        data.append("username", username.current.value);
        data.append("password1", password.current.value);
        data.append("password2", password2.current.value);
        axios.post("http://127.0.0.1:8000/rest-auth/registration/", data).then((res) => console.log(res))
            .catch((error) => prompt(error.message))

    };
    return(<Form onSubmit={(e) => onSubmit(e)}>
        <h2>Sign Up</h2>
        <Form.Group>
            <Form.Label>Email</Form.Label>
            <Form.Control type="email" ref={email}/>
        </Form.Group>
        <Form.Group>
            <Form.Label>UserName</Form.Label>
            <Form.Control type="text" ref={username}/>
        </Form.Group>
        <Form.Group>
            <Form.Label>Password</Form.Label>
            <Form.Control type="password" ref={password}/>
        </Form.Group>
        <Form.Group>
            <Form.Label>Confirm Password</Form.Label>
            <Form.Control type="password" ref={password2}/>
        </Form.Group>
        <Button type="submit">Submit</Button>
    </Form>)
};

export const ForgetPassword = () => {
    const password = useRef(null);
    const password1 = useRef(null);
    const {user} = useUser();
    const onSubmit = (e) => {
        e.preventDefault();
        let data = new FormData();
        data.append('new_password1', password.current.value);
        data.append("new_password2", password1.current.value);
        data.append("old_password", );
        axios.post("http://127.0.0.1:8000/rest-auth/password/change/", data,{
            headers:{ 'Authorization' :  `Token ${user.token}` }
        }).then((res) => console.log(res)).catch((error) =>  alert(error.message))
    }
    return(<Form onSubmit={(e) => onSubmit(e)}>
        <Form.Group>
            <Form.Label>Password</Form.Label>
            <Form.Control type="password" ref={password}/>
        </Form.Group>
        <Form.Group>
            <Form.Label>Confirm Password</Form.Label>
            <Form.Control type="password" ref={password1}/>
        </Form.Group>
        <Button type="submit">Submit</Button>
    </Form>)

};

export const AccountPage = () => {
    const {user} = useUser();

    return(<Container>
        <h2>Welcome to Your Account Page: {user.username}</h2>
        <span><Link to={RoutesE.forget}>Forget Password?</Link></span>

    </Container>)

};

export const SignOut = () => {
    const {SignOut} = useUser();
    const navigate = useNavigate();
    useEffect(() => {
        SignOut();
        navigate("/")

    }, []);

    return(<></>)
}