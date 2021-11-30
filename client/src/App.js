import logo from './logo.svg';
import React from "react";
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import {Container} from "react-bootstrap";
import UploadForm from "./components/uploadForm";
import SeedProvider from "./context/seedContext";
import Navi from "./components/topNav";
import * as RoutesE from "./routes"
import {Route, Routes} from "react-router-dom";
import Home from "./components/home";
import {AccountPage, ForgetPassword, SignIn, SignOut, SignUp} from "./components/account";
import {useUser} from "./context/userContext";
function App() {

  return (
    <Container className="Home">
        <SeedProvider>
            <Navi/>
            <Routes>
                <Route exact path={RoutesE.home} element={<Home/>}/>
                <Route path={RoutesE.embed}/>
                <Route path={RoutesE.upload} element={<UploadForm/>}/>
                <Route path={RoutesE.signin} element={<SignIn/>}/>
                <Route path={RoutesE.signup} element={<SignUp/>}/>
                <Route path={RoutesE.forget} element={<ForgetPassword/>}/>
                <Route path={RoutesE.account} element={<AccountPage/>}/>
                <Route path={RoutesE.signout} element={<SignOut/>}/>
            </Routes>

        </SeedProvider>
    </Container>
  );
}

export default App;
