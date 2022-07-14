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









// Create a theme instance.
// const theme = createTheme({
//   palette: {
//     primary: {
//       main: '#556cd6',
//     },
//     secondary: {
//       main: '#19857b',
//     },
//     error: {
//       main: colors.red.A400,
//     },
//   },
// });

// function LightBulbIcon(props) {
//   return (
//     <SvgIcon {...props}>
//       <path d="M9 21c0 .55.45 1 1 1h4c.55 0 1-.45 1-1v-1H9v1zm3-19C8.14 2 5 5.14 5 9c0 2.38 1.19 4.47 3 5.74V17c0 .55.45 1 1 1h6c.55 0 1-.45 1-1v-2.26c1.81-1.27 3-3.36 3-5.74 0-3.86-3.14-7-7-7zm2.85 11.1l-.85.6V16h-4v-2.3l-.85-.6C7.8 12.16 7 10.63 7 9c0-2.76 2.24-5 5-5s5 2.24 5 5c0 1.63-.8 3.16-2.15 4.1z" />
//     </SvgIcon>
//   );
// }

// function ProTip() {
//   return (
//     <Typography sx={{ mt: 6, mb: 3 }} color="text.secondary">
//       <LightBulbIcon sx={{ mr: 1, verticalAlign: 'top' }} />
//       Pro tip: See more{' '}
//       <Link href="https://mui.com/getting-started/templates/">templates</Link> on the MUI
//       documentation.
//     </Typography>
//   );
// }

// function Copyright() {
//   return (
//     <Typography variant="body2" color="text.secondary" align="center">
//       {'Copyright © '}
//       <Link color="inherit" href="https://mui.com/">
//         Your Website
//       </Link>{' '}
//       {new Date().getFullYear()}
//       {'.'}
//     </Typography>
//   );
// }

// function App() {
//   return (
//     <Container maxWidth="sm">
//       <Box sx={{ my: 4 }}>
//         <Typography variant="h4" component="h1" gutterBottom>
//           CDN example
//         </Typography>
//         <ProTip />
//         <Copyright />
//       </Box>
//     </Container>
//   );
// }

// const root2 = ReactDOM.createRoot(document.getElementById('root'));
// root2.render(
//   <ThemeProvider theme={theme}>
//     {/* CssBaseline kickstart an elegant, consistent, and simple baseline to build upon. */}
//     <CssBaseline />
//     <App />
//   </ThemeProvider>,
// );

































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
        <div >{label}</div>
        <div className={'ident'}>{children}</div>
      </div>);
  }
}


class DynamicList extends React.Component {
  render() {
    // data is the list
    const data = this.props.data;
    // in children there should be how a single list element should look
    const children = this.props.children;

    return (
      <div>
        {data.map((listElement) =>
          React.Children.only(React.cloneElement(children, { data: listElement })) // TODO: Kein key
        )}
        <button>Add element</button>
      </div>);
  }
}


class XYZ extends React.Component {
  render() {
    // data is the list
    const data = this.props.data;
    // in children there should be how a single list element should look
    const children = this.props.children;

    return (
      <div>
        {data.map((listElement) =>
          React.Children.only(React.cloneElement(children, { data: listElement })) // TODO: Kein key
        )}
        <button>Add element</button>
      </div>);
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
    <Box sx={{ width: 300 }}>
      <Slider
        getAriaLabel={() => 'Temperature range'}
        value={value}
        onChange={handleChange}
        getAriaValueText={(a) => "valuetext"}
        min={0}
        max={10}
        valueLabelDisplay="auto"
        marks={marks}
      />
    </Box>
  );
}





const root = ReactDOM.createRoot(
    document.getElementById('root')
);
root.render( (
  <Group label="ddd">
    <DynamicList data={[1,2,3]}>
      <a><input type="file" /><RangeSlider
        getAriaLabel={() => 'Temperature range'}
        value={[5,7]}
        min={0}
        max={10}
      />
      </a>
    </DynamicList>
  </Group>




));

