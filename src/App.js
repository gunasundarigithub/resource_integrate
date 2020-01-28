import React from 'react';
import logo from './logo.svg';
import './App.css';
import SearchAppBar from './SearchAppBar.js'
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import Button from '@material-ui/core/Button';
import Table from './Components/Table';


class App extends React.Component{

State= {
  showTable:false
    }


render(){

const team_list = [
  { team_name:'team-1', team_id: 1 },
  { team_name: 'team-2', team_id: 2 },
  { team_name: 'team-3', team_id: 3 },
  { team_name: 'team-4', team_id: 4 },
];


 //const [showTable, setShowTable] = useState(false);

return (
  <div className="App">
      <SearchAppBar/>
      <br/><br/>  
      <div style={{ display: 'inline-flex' }}>
      <div> <Autocomplete display="inline"
      style={{ width: 350, float :"left"}}
      options={team_list.map(option => option.team_name)}
        renderInput={params => (
          <TextField {...params} label="Enterprise_teams" color="secondary"  variant='outlined' style={{ width: 300}} />
        )}/> 
  <Button variant="contained" display='inline' color="secondary"   onClick={() => {this.setState({showTable:true})} }>
  Create/edit/view schedule
</Button>
    </div></div>
{this.state.showTable ? <div><Table></Table></div> : null }
</div>
     );
}
}
export default App;
