import React from 'react'
import {Container} from "react-bootstrap"
import {useUser} from "../context/userContext";
import {useCanvas} from "../hooks/useCanvas";

export default function Home(){
    const {user} = useUser();


    return(<Container>
        <h2>Welcome To Fish Eye</h2>
        <span>Fish Eye is a Website Build With React JS and Django</span>
    </Container>)
}