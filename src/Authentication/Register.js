import React, { Component } from 'react';
 import {TextField,Button,FormGroup,Container,Grid,AppBar,Toolbar,Typography,IconButton} from '@material-ui/core';


export default class Login extends Component {

render(){
  return (
    <div className="App">
        <AppBar position="static">
        <Toolbar variant="dense">
          <IconButton edge="start" color="inherit">
          </IconButton>
          <Typography variant="h6" color="inherit">
            Resource scheduler 
          </Typography>
        </Toolbar>
        </AppBar>
<Grid
  container
  spacing={0}
  direction="column"
  alignItems="center"
  justify="center"
  style={{ minHeight: '85vh' }}>

  <form>
      <h2>Login to your account</h2>
      <div>
        <TextField type='email' label="Registered Email" variant="outlined"/>
        <br/> <br/>
        <TextField type='password'  label="Password" variant="outlined"/>
        <br/><br/>
        <Button color="primary" variant="contained">Login</Button>
        <br/><br/>
        <h3>Don't have an account ? <Button color="purple" variant="contained">Register</Button> </h3>
        </div> 
      </form>
  </Grid>    
        
    </div>
  );
}
}

