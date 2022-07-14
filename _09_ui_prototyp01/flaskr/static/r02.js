'use strict';
const {
  colors,
  CssBaseline,
  ThemeProvider,
  Typography,
  Container,
  createTheme,
  Box,
  SvgIcon,
  Link,
  Slider
} = MaterialUI;




let data = {
  objects_to_recognize: [
    {
      url: "",
      min: 3,
      max: 4
    }
  ],
  area_length_x: 3,
  area_length_y: 7,
  camera_height: 5
};




class Group extends React.Component {
  render() {
    const label = this.props.label;
    const children = this.props.children;

    return (
      <div >
        <div className={"group-label"}>{label}</div>
        <div className={'ident group-child-container'}>{children}</div>
      </div>);
  }
}


class DynamicList extends React.Component {

  key = 0;
  getKey() {
    this.key += 1;
    return this.key;
  }

  render() {
    // data is the list
    const data = this.props.data;
    this.keys = data.map( (a) => this.getKey() )

    // in children there should be how a single list element should look
    const children = this.props.children;

    return (
      <div className={"dynamic-list-container"}>
        {data.map((listElement, index) =>
          React.Children.only(React.cloneElement(children, { data: listElement, key: this.keys[index] })) // TODO: Kein key
        )}
        <button>Add element</button>
      </div>);
  }
}


class ObjectBox extends React.Component {
  render() {
    return (
      <Box sx={{ display:"flex", flexDirection:"column", gap:"20px" }} className={'object-box'}>
        <div>
          <Group label="3D-Modell"/>
          <input type="file" />
        </div>
        <div>
          <Group label="Wieviele Objekte dieses Typs pro Bild"/>
          <RangeSlider value={[5,7]} min={0} max={10} />
        </div>
    </Box>
    );
  }

}




function RangeSlider() {
  const [value, setValue] = React.useState([5, 5]);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  const marks = [
    {
      value: 0,
      label: '0',
    },
    {
      value: 10,
      label: '10',
    }]  

  return (
      <Slider
        value={value}
        onChange={handleChange}
        getAriaValueText={(a) => "valuetext"}
        min={0}
        max={10}
        valueLabelDisplay="auto"
        marks={marks}
      />
  );
}





class NumberInputWithUnit extends React.Component {
  render() {
    const label = this.props.label;
    const unit = this.props.unit;
    const value = this.props.value;

    return (
      <div className={"number-input-with-unit-container"}>
        <div>{label}:</div>
        <input type="number" value={value}/>
        <div>{unit}</div>
      </div>);
  }
}





const root = ReactDOM.createRoot(
    document.getElementById('root')
);
root.render( (
  <Box sx={{width:'800px', marginLeft:'auto', marginRight:'auto'}}>
    <Group label="Zu erkennende Objekte">
      <DynamicList data={[1,2,3]}>
        <ObjectBox />
      </DynamicList>
    </Group>

    <Group label="Szene modellieren">
      <Group label="Bereich, in dem alle Objekte erscheinen">
        <NumberInputWithUnit label={"Länge in x-Richtung"} unit={"cm"} value={data.area_length_x} />
        <NumberInputWithUnit label={"Länge in y-Richtung"} unit={"cm"} value={data.area_length_y} />
      </Group>
      <Group label="Kamera">
        <NumberInputWithUnit label={"Höhe über Tisch"} unit={"cm"} value={data.camera_height} />
      </Group>
    </Group>

  </Box>

));

