function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
} 

const HOST = "http://127.0.0.1:8000"

// Controls whether managing employees or managing positions
class EmployeeManagement extends React.Component{
    constructor(props){
        super(props)  
        this.state={
            page : 'employee_management', 
            positions:[]     
        }  
    }
    
    render(){
        return(
            <div>
                {/* Change page view from employee management to position management */}
                <div className="row container-center-row">
                    <button onClick={this.change_view} className="col-md-4 btn btn-page-view btn-lg btn-info " name="employee_management">Employees</button>
                    <button onClick={this.change_view} className="col-md-4 btn btn-page-view btn-lg" name="position_management">Positions</button>  
                </div>  

                <div>
                    {this.state.page === "employee_management"?
                            <EmployeeControl
                                key = {this.state.positions}
                                positions = {this.state.positions}
                            />   
                        : 
                            <PositionControl 
                                key = {this.state.positions}
                                positions = {this.state.positions}
                                get_positions = {this.get_positions}
                            />                  
                    }                        
                </div>          
            </div>              
        )
    }
       

    // Change the current page view
    change_view=(event)=>{
        // Change previous selection to without highlight
        var current_button = document.getElementsByName(`${this.state.page}`)[0]
        current_button.classList.remove("btn-info")
        
        // Change page view
        this.setState({
            page : event.target.name
        })

        // Add highlight to page selected
        event.target.classList.add("btn-info")
    }

    componentDidMount=()=>{
        this.get_positions()
    }
    
    // Get all created positions of business
    get_positions=()=>{
        fetch(`${HOST}/business/${business_name}/employee_management/positions/`)
        .then(response=>{
            // console.log(response)
            if(response.status === 200){
                return response.json()
            }
        })
        .then(response=>{
            if(response){
                // console.log(response)
                this.setState({
                    positions:response
                })
            }
        })
    }
}


// Manage employees, view, delete and change positions
class EmployeeControl extends React.Component{
    constructor(props){
        super(props)  
        this.state={
            add_employee:false,
            warning_message:"",
            employees:[],
            edit:"",   
            position_change:"",
            pagination:{
                has_next:false,
                has_previous:false,
                num_pages:"",
                number:"",
                next_page_number:"",
                previous_page_number:""

            }, 
            query:""      
        }  
    }
    render(){
       
        let all_employees = this.create_employees_section()
        return(
            <div>
                {/* Add employee form */}
                <div>            
                    {this.state.add_employee?

                        <div className = "container-center-column container-overlay">
                            <div className="form-group">
                                <h2 style={{color:"red"}}>{this.state.warning_message}</h2>
                            </div>
                            <div className="form-box-small" style={{backgroundColor:"white",opacity:".89"}}>
                                <div className='container-center-column'>
                                    <div className="form-group">
                                        <input className="form-control" type="text" id="new_employee_username" placeholder="employee username" size='80' ></input>
                                    </div>
                                    <div className="form-group">
                                        <button className="form-control btn btn-lg btn-success" style={{color:"white"}} onClick={this.add_employee} name="add_new_employee">Add</button>
                                    </div>

                                    <div>
                                        <button className="btn btn-danger" style={{color:"white"}} onClick={this.handleChange} name="close_employee_add_form">Close</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                            
                    :   
                        false
                    }
                </div>
                <div className="container-center-column lone-btn" >
                            <button className="btn btn-primary btn-lg " onClick={this.handleChange} name="open_employee_add_form" >Add New Employee</button>
                        </div>
                <div className="container-center-row">
                    <div className="search-box" style={{width:"70%"}}>    
                        <input className="form-control" name="query_search" onChange={this.handleChange} type="text" placeholder="search"></input>
                        <button type="submit" name="search_button" onClick={()=>this.get_employees(1)}><i className="form-control fa fa-search"></i></button>   
                    </div>
                </div>

                {/* Display employees  */}
                <div >
                    <div className="index-container">
                        <div className="row">
                            {this.state.employees?
                                all_employees
                                :
                                false
                            }
                        </div>
                    </div>

                    {/* Pagnition */}
                    <div>
                        <span className="step-links">
                            <ul className="pagination" style={{ justifyContent: 'center',}} >
                                {this.state.pagination.has_previous ?

                                    <React.Fragment>
                                        <button className="page-link"  onClick={this.change_page} value={1} > first</button> 
                                        <button className="page-link"  onClick={this.change_page} value={this.state.pagination.previous_page_number} >previous</button>
                                    </React.Fragment>

                                    : <h1></h1> 
                                }
                                
                                    <span className="current" style={{marginLeft:"10px",marginRight:"10px",marginTop:"10px"}} >
                                        Page { this.state.pagination.number}  of  {this.state.pagination.num_pages}
                                    </span>

                                { this.state.pagination.has_next ? 
                                    <React.Fragment> 
                                        <button className="page-link" onClick={this.change_page} value={this.state.pagination.next_page_number}  >next</button> 
                                        <button className="page-link" onClick={this.change_page} value={this.state.pagination.num_pages} >last </button>
                                    </React.Fragment>

                                : <h1></h1>
                                }
                            </ul>
                        </span>
                    </div>
                </div>
            </div>
        ) 
    }
    componentDidMount=()=>{
        this.get_employees(1) 
    }
    change_page = (event) =>{
        // console.log(event.target.value)
        this.get_employees(event.target.value)
    }
    
    // Get all employeees of the business with or without query and set pagnition
    get_employees=(page_num)=>{
        var query = "all"
        if(this.state.query.trim()){
            query = this.state.query
        }
        fetch(`${HOST}/business/${business_name}/employee_management/employees/${query}/${page_num}/`)
        .then(response=>{
            // console.log(response)
            if(response.status === 200){
                return response.json()
            }
        })
        .then(response=>{
            // console.log(response)
            if(response){
                this.setState({
                    employees:response[0],
                    pagination:{
                        has_next:             response[1][0].has_next,
                        has_previous:         response[1][0].has_previous,
                        num_pages:             response[1][0].num_pages,
                        number:               response[1][0].number,
                        next_page_number:      response[1][0].next_page_number,
                        previous_page_number:  response[1][0].previous_page_number,
                    }
                })
            }
        })
    }
    
    // Manages how employees should be displayed whether viewing or editing
    create_employees_section=()=>{
        var employees_table = this.state.employees.map(employee=>{  
            let position_selection = this.render_position_options(employee.position)
            return(
                <div key = {employee.id} className="col-md-4 ">
                    <div className="employee-card">
                        <div className="image">
                            {employee.image?
                                <img src={employee.image}></img>
                                :
                                false
                            }
                        </div>

                        <div className="name">
                            <h3>
                                {employee.name}
                            </h3>
                        </div>

                        {this.state.edit === employee.id ?
                            <div className="position edit_position" style={{textTransform:"capitalize"}}>
                                <select name="employee_position_selector" className='form-control select-position' onChange={this.handleChange} defaultValue={employee.position} >
                                    <option key="none" value="none">NONE</option>
                                    {position_selection}
                                </select>
                                <div className='container-center-row' style={{marginBottom:"2em",marginTop:"2em"}} >
                                    <button className="btn btn-success" onClick={this.change_employee_position} style={{marginRight:"1em"}}>Save</button>
                                    <button className="btn btn-danger" onClick={this.delete_employee}>Remove Employee</button>
                                </div>
                            </div>

                        :
                            <div className = "footer">
                                <div className="position" style={{marginBottom:"1em"}}>
                                    <h4>{employee.position}</h4>
                                </div>
                                <div className="container-center-row line-btn" >
                                        <button className="btn btn-primary" onClick={()=>this.edit_employee(employee.id)}>Edit</button>
                                </div>
                            </div>   
                        }
                    </div>        
                </div>
            ) 
        })  
        if(employees_table.length > 0){
            return employees_table    
        }
        return(
            <div className="col-md-12">
                <h2 className="text-center">No Employees</h2>
            </div>
        ) 
    }

    // Change employee to be edited
    edit_employee=(employee_id)=>{
        this.setState({
            edit:employee_id,
            position_change:""
        })
        this.get_employees(this.state.pagination.number)
    }
    
    // Adds position options for assignment to employees
    render_position_options(position_held){
            
        let position_options = this.props.positions.map((position, index) =>{

            if(position_held === "position"){
                return <option key={index} value={position.name} selected>{position.name.toUpperCase()}</option>
            }else{
                return <option key={index} value={position.name}>{position.name.toUpperCase()}</option>
            }
        })
        return position_options        
    }

    // Adds a new employee to business database using username
    add_employee=()=>{   
        if (confirm('Are you sure you want to add this employee?')){      
            var employee_username = document.querySelector('#new_employee_username').value
            if (employee_username){
                // console.log(employee_username)
                fetch(`${HOST}/business/${business_name}/employee_management/employees/none/0/`,{
                    method:'POST',
                    body: JSON.stringify({
                        'employee_username': employee_username,
                    }),
                
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken")
                    }
                })
                .then(response=>{
                    if (response.status === 200){
                        // console.log("added new employee")
                        this.get_employees(this.state.pagination.number)
                        this.setState({
                            add_employee:false,
                            warning_message:""
                        })
                    }
                    else{
                        this.setState({
                            warning_message:"Invalid Username"
                        })
                    }
                })
            }   
        } else{
             // Do nothing!
             console.log('cancelled');
        } 
    }
    
    // Deletes an employee from business database
    delete_employee=()=>{
        console.log("delete employee")
        if (confirm('Are you sure you want to add this employee?')){  
            fetch(`${HOST}/business/${business_name}/employee_management/employees/none/0/`,{
                method:'DELETE',
                body: JSON.stringify({
                    'employee_id': this.state.edit,
                }),
            
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                }
            })
            .then(response=>{ 
                if(response.status === 200){
                    this.get_employees(this.state.pagination.number)
                    alert("Successfully removed employee")
                }
                else{
                    alert("Failed")
                }
            })
        }else{
            // Do nothing!
            console.log('cancelled');
        }
        this.setState({
            edit:"",
            position_change:""
        })
    }
    
    // Changes employee's position in business database
    change_employee_position=()=>{
        if (confirm('Are you sure you want to save changes?')){  
            if(this.state.position_change){
                // console.log("change employee position", this.state.position_change )
                fetch(`${HOST}/business/${business_name}/employee_management/employees/none/0/`,{
                    method:'PUT',
                    body: JSON.stringify({
                        'employee_id': this.state.edit,
                        'position': this.state.position_change
                    }),
                
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken")
                    }
                })
                .then(response=>{ 
                    if(response.status === 200){
                        this.get_employees(this.state.pagination.number)
                        alert("Successfully changed position")
                    }
                })
            }
            
        }else{
            // Do nothing!
            console.log('cancelled');
        }
        this.setState({
            edit:"",
            position_change:""
        })
    }
    
    handleChange=(event)=>{
        // console.log(event.target.value)
        
        if(event.target.name === "open_employee_add_form"){
            this.setState({
                add_employee: true

            })
        }
        else if(event.target.name === "close_employee_add_form"){
            this.setState({
                add_employee:false,
                warning_message:""
            })
        }
        else if(event.target.name === "employee_position_selector"){
            this.setState({
                position_change : event.target.value
            })
        }
        else if(event.target.name == "query_search"){
            this.setState({
                query : event.target.value
            })
        }
        
    }
}

// Manages position creation and permissions assignment to position
class PositionControl extends React.Component{
    constructor(props){
        super(props)  
        this.state={
            add_position:false,
            warning_message:"",
            display:3,
            length_of_list:0,
            pagination:{
                has_next:false,
                has_previous:false,
                num_pages:"",
                page_number:"",
            }, 
            query:""  
        }  
    }

    render(){
        let all_positions = this.render_positions_section()
        return(
            <div>
                {/* Position add form */}
                <div>
                    {this.state.add_position?
                        <div className = "container-center-column container-overlay">
                            <div className="form-group">
                                 <h2 style={{color:"red"}}>{this.state.warning_message}</h2>
                            </div>
                            <div className="form-box-small" style={{backgroundColor:"white",opacity:".89"}}>
                                <div className ="container-center-column">
                                    <div className="form-group">
                                        <input className="form-control" type="text" id="new_position_input" placeholder="position" size='80'></input>
                                    </div>
                                    <div className="form-group">
                                        <button className="form-control btn btn-lg btn-success" style={{color:"white"}} onClick={this.add_position}>Add</button>
                                    </div>
                                    <div>
                                        <button className="btn btn-danger" style={{color:"white"}} onClick={this.handleChange} name="close_add_positions_form">Close</button>
                                    </div>
                                </div>
                            </div>
                        </div>   
                    : 
                        false
                    }
                </div>

                <div className="container-center-column lone-btn" >
                    <button className="btn btn-primary btn-lg" onClick={this.handleChange} name="open_add_positions_form">Add New Position</button>
                </div>

                {/* Display all positions with permissions assigned */}
                <div>
                    <div className="index-container">
                        <div className="row">
                            { this.props.positions?
                                all_positions     
                            :
                                false
                            }  
                        </div>
                    </div>
                </div>
                
                {/* Pagnition */}
                <div className="conatiner-fluid">
                    <div className="container-center-row" >
                        <div style={{marginRight:"1em"}}>
                            {this.state.pagination.has_previous?
                                <button className="btn btn-primary btn-lg" onClick={()=>{this.change_page_num(-1)}}>prev</button>
                                :
                                <button className="btn btn-lg">prev</button>
                            }
                        </div>
                        page {this.state.pagination.page_number}
                        <div style={{marginLeft:"1em"}}>
                            {this.state.pagination.has_next?
                                <button className="btn btn-primary btn-lg" onClick={()=>{this.change_page_num(1)}}>next</button>
                                :
                                <button className="btn btn-lg">next</button>
                            }
                        </div>
                    </div>
                </div>
            </div>
        )
    }

    // How positions are displayed
    render_positions_section=()=>{
        // console.log(this.state.length_of_list, this.state.pagination.page_number, this.state.display)
        var begin = (this.state.pagination.page_number - 1) *  this.state.display
        var end = this.state.pagination.page_number *  this.state.display
        // console.log(begin,end)
        var positions_section = this.props.positions.map((position,index)=>{  
            // console.log(index)
            if(index >= begin && index < end){
                return(
                    <Position 
                    key={position.id}
                    position={position.name}
                    permissions ={position.permissions}
                    permission_control = {this.permission_control}
                    delete_position = {this.delete_position}
                    />
                ) 
            }
        })  
        if(positions_section.length > 0){
            return positions_section    
        }
        return(
            <div className="col-md-12">
                <h2 className="text-center">No Positions</h2>
            </div>
        )
    }

    componentDidMount=()=>{
        var next = false
        var length_positions_array = this.props.positions.length
        var number_of_pages = Math.ceil(length_positions_array/this.state.display)
        // console.log(number_of_pages)
        
        if(length_positions_array > this.state.display){
            var next = true
        }

        this.setState({
            length_of_list : length_positions_array,
            pagination:{
                has_next: next,
                has_previous: false,
                page_number: 1,
                num_pages:number_of_pages,
            }
        })
    }

    // Pagnition change
    change_page_num =(num)=>{
        // If next add 1 and if previous less 1 from current page number
        var new_page_number = this.state.pagination.page_number + num
        var has_next = true
        var has_previous = true

        // console.log(this.state.pagination)

        // If the page number to go to is less than page 1 set the page number to page 1
        if (new_page_number <= 1){
            new_page_number = 1
            has_previous = false
        }
        // If the page number to go to is greater than last page set to last page
        else if (new_page_number >= this.state.pagination.num_pages){
            new_page_number = this.state.pagination.num_pages
            has_next = false
        }

        this.setState({
            pagination:{
                has_next: has_next,
                has_previous: has_previous,
                page_number:new_page_number,
                num_pages: this.state.pagination.num_pages
            }
        })
        // console.log(this.state.pagination.page_number)
    }
    
    // Add new position to business
    add_position=()=>{
        if (confirm('Are you sure you want to add position?')){
            var new_position = document.querySelector('#new_position_input').value
            if (new_position){
                // console.log(employee_username)
                fetch(`${HOST}/business/${business_name}/employee_management/positions/`,{
                    method:'POST',
                    body: JSON.stringify({
                        'position': new_position,
                    }),
                
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken")
                    }
                })
                .then(response=>{
                    if (response.status === 200){
                        // console.log("added new employee")
                        this.setState({
                            add_position:false,
                            warning_message:""
                        })
                        this.props.get_positions()
                    }
                    else{
                        this.setState({
                            warning_message:"Invalid Position"
                        })
                    }
                })
            } 
        }
    }

    // Delete a position
    delete_position=(position)=>{
        if (confirm('Are you sure you want to delete position?')){
            console.log("delete position")
            fetch(`${HOST}/business/${business_name}/employee_management/positions/`,{
                method:'DELETE',
                body: JSON.stringify({
                    'position': position,
                }),
            
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                }
            })
            .then(response=>{ 
                if(response.status === 200){
                    this.props.get_positions()
                    alert("Successfully deleted position")
                }
                else{
                    alert("FAILED")
                }
            })
        }
    }

    
    handleChange=(event)=>{
        // console.log(event.target.value)
        if(event.target.name === "open_add_positions_form"){
            this.setState({
                add_position: true

            })
        }
        else if(event.target.name === "close_add_positions_form"){
            this.setState({
                add_position:false,
                warning_message:""
            })
        }
        else if(event.target.name == "query_search"){
            this.setState({
                query : event.target.value
            })
        }
    }  
    
    // Adds or revokes permissions to a position
    permission_control=(action,position,permission)=>{
        if (confirm(`Are you sure you want to ${action} ${permission} to ${position} ?`)){
            fetch(`${HOST}/business/${business_name}/employee_management/positions/`,{
                method:'PUT',
                body: JSON.stringify({
                    'action': action,
                    'position': position,
                    'permission': permission
                }),
            
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                }
            })
            .then(response=>{
                if(response.status === 200){
                    this.props.get_positions()
                }
                else{
                    alert("Could not carrry out action")
                }
            })
        }
    }
}

// Displays position and permissions assigned
class Position extends React.Component{
    constructor(props){
        super(props)  
        this.state={
            all_permissions:[
                'access inventory',
                'manage inventory',
                'make sales',
                'access accounts', 
                'manage accounts',
                'manage employees',
            ],
        }
    }
    
    render(){
        let permissions_section = this.permissions_section()
        return(
            <div className="col-md-4">
                <div className="position-card">
                    <div className="text-center position-name">
                        <h2>{this.props.position}</h2>
                    </div>
                    <div className="permissions">   
                        {permissions_section}
                    </div>

                    <div className = "container-center-row lone-btn">
                        <button className="btn btn-danger" onClick={()=> this.props.delete_position(this.props.position)}>Delete Position</button>
                    </div>
                </div>
            </div>
        )
    }
    
    // Displays which positions are allowed and which are denied
    permissions_section=()=>{
        // console.log(this.props.permissions)
        var permissions = this.state.all_permissions.map(permission=>{  
            var length = this.props.permissions.length
            var permission_granted = false

            for(var i=0; i < length ; i++){
                // console.log(this.props.permissions[i].permission, permission)
                if(this.props.permissions[i].permission === permission){
                    // console.log(permission)
                    permission_granted = true
                    break
                }
            }

            return(
                <div key = {permission} className="permissions-row" >
                    {permission_granted ?
                        <p style={{color:"green"}}>
                            {permission}    
                        </p>
                    :
                        <p style={{color:"red"}}>
                            {permission}        
                        </p>
                    }

                    <div>
                        {permission_granted ?
                            <div>
                                <div style={{width:"250px"}} >
                                        <label className="switch">
                                            <input type="checkbox" onChange={()=>this.props.permission_control("revoke",this.props.position,permission)} defaultChecked></input>
                                            <span className="slider round"></span>
                                        </label>
                                    </div>  
                            </div>
                            :
                            <div>  
                                <div style={{width:"250px"}}>
                                    <label className="switch">
                                        <input type="checkbox" onChange={()=>this.props.permission_control("add",this.props.position,permission)} ></input>
                                        <span className="slider round"></span>
                                    </label>
                                </div>  
                            </div> 
                        }
                    </div> 
                </div>
            ) 
        })  
        return permissions  
    }
}

ReactDOM.render(<EmployeeManagement />,document.querySelector('#body'));   
// console.log(business_name)
