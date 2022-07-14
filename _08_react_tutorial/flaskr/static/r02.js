//'use strict';




// function getMyFavoriteElement(props) {
function GetMyFavoriteElement(props) {
    //console.log(props);
    const name = 'Josh Perez';
    const element = <h1>Hello, {props.value}</h1>;
    return element
}


class Welcome extends React.Component {

    constructor (props) {
        super(props);
        this.state = {number : 10};
    }


    componentDidMount() {
        this.timerID = setInterval(
          () => this.tick(),
          1000
        );
      }

      componentWillUnmount() {
        clearInterval(this.timerID);
      }


      tick() {
        // First attempt, but actually should be different:
        //let old = this.state.number;
        ////this.state = {number : old + 1};
        // this.setState(
        //     {number : old + 1}
        // )
        // Second attempt:
        this.setState( (state, props) =>
            ({number : state.number + 2})
        )

      }


    render() {
      return <h1>WeLcOmE, {this.props.name} and {this.state.number} </h1>;
    }





    
  }



const root = ReactDOM.createRoot(
    document.getElementById('root')
);
root.render(  GetMyFavoriteElement({value:"aaa"})  );
root.render(  GetMyFavoriteElement({value:"bbb"})  );
root.render(  GetMyFavoriteElement({value:"ccc"})  );
root.render(  <GetMyFavoriteElement value="ddd" />  );
// root.render(  new Welcome().render({name:"lol"})  );
root.render(   <Welcome name="ddd" /> );




