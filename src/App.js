import React from 'react';
import './App.css';
import SearchAppBar from './SearchAppBar.js'
import Button from '@material-ui/core/Button';
import Table from './Components/Table';
import Select from './Components/MaterialUI/Select'; 


class App extends React.Component{

state= {
  showTable:false, //to show the table after clicking on the button
  showButton:false, //to show the button after clicking on the team from the drop down
  selectedTeam: '', //selected value from the drop down
   }

handleChange = (event,value) => {
  console.log(event.target.value);
  console.log(event)
  console.log(value)
    this.setState({ selectedTeam: event.target.value,showButton: true });
  }

render(){

const team_list = [
  { team_name:'Ent_digital', team_id: 1 },
  { team_name: 'Auto_Exp', team_id: 2 },
  { team_name: 'ECT', team_id: 3 },
  { team_name: 'EFT', team_id: 4 },
];
//const [showTable, setShowTable] = useState(false);

return (
  
  <Home/>

<div className="App">
      <SearchAppBar/> 
      <div style={{width:'950px' }}>
      <div>
      <br/>
      <Select title="Enterprise Teams" change={this.handleChange} items={team_list} selectedName={this.state.selectedTeam}   />
    { this.state.showButton ? <Button variant="contained" color="secondary"  className="bStyle" onClick={() => {this.setState({showTable:true})} }>
       Create/edit/view schedule
     </Button> :null }
    </div>
    </div>
{this.state.showTable ? <div style={{display: 'inline-flex', justifyContent:'center', alignItems:'center', height: '500px'}}><Table></Table></div> : null }
</div>
     );
}
}
export default App;
