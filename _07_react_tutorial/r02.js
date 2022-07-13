'use strict';


const name = 'Josh Perez';
const element = <h1>Hello, {name}</h1>;






const domContainer = document.querySelector('#like_button_container');
const root = ReactDOM.createRoot(domContainer);
root.render(element);




