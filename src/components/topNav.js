import React from "react";
import {Navbar, Container, Nav} from "react-bootstrap";
import {Link} from "react-router-dom"
import * as RoutesE from "../routes"
import {useUser} from "../context/userContext";
export default function Navi() {
    const {user} = useUser();

    return(<Navbar bg="light" expand="lg">
        <Container>
            <Navbar.Brand>Fish Eye</Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="me-auto">
                    <Nav.Link as={Link} to={RoutesE.home}>Home</Nav.Link>
                    <Nav.Link as={Link} to={RoutesE.upload}>Upload</Nav.Link>
                    <Nav.Link as={Link} to={RoutesE.embed}>Embed</Nav.Link>
                    {user !== null ?<Nav.Link as={Link} to={RoutesE.account}>Account</Nav.Link>: <Nav.Link as={Link} to={RoutesE.signin}>Sign In</Nav.Link>}
                    {user !== null && <Nav.Link as={Link} to={RoutesE.signout}>Sign Out</Nav.Link>}
                </Nav>
            </Navbar.Collapse>
        </Container>
    </Navbar>)
}