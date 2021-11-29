import React, {Component} from 'react'

export default class ErrorBoundary extends Component{
    state = {error: null};
    static getDerivedStateFromError(error){
        return {error}
    }
    render(){
        console.log(this.state);
        const {error} = this.state;
        const {children} = this.props;

        if(error) return <ErrorScreen error={error}/>;
        return children;
    }
}

export function ErrorScreen({error}) {
    return(<div>
        <p>Error: {error.message}</p>
    </div>)
}