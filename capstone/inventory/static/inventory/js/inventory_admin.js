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

// Manage business inventory, edit, delete
class InventoryManagement extends React.Component{
    constructor(props){
        super(props)
        this.state = {
            all_inventory:[],
            edit:"",
            inventory_query:"",
            inventory_pagination:{
                has_next:false,
                has_previous:false,
                num_pages:"",
                number:"",
                next_page_number:"",
                previous_page_number:""
            },
        }
    }

    render(){
        let all_inventory = this.mapInventoryItems()
        return(
            <div>
                <div className="container-fluid container-center-row search-box" style={{width:"70%"}}>
                    <input type="search" className="form-control rounded" placeholder="Search" name="query-inventory" onChange={this.handleChange}></input>
                    <button type="submit" className="btn btn-outline-primary" name="submit-query"  onClick={this.handleClick}>
                        Search
                    </button>
                </div> 
                 {/*Display all inventory  */}
                <div className="container-fluid">   
                    <div className="index-inventory">
                        <div className="row">       
                            {all_inventory}
                        </div>
                    </div>
                </div> 
                {/* Pagnition */}
                <div>
                    <span className="step-links">
                        <ul className="pagination" style={{ justifyContent: 'center',}} >
                            {this.state.inventory_pagination.has_previous ?

                                <React.Fragment>
                                    <button className="page-link"  onClick={this.change_page} value={1} > first</button> 
                                    <button className="page-link"  onClick={this.change_page} value={this.state.inventory_pagination.previous_page_number} >previous</button>
                                </React.Fragment>

                                : <h1></h1> 
                            }
                            
                                <span className="current" style={{marginLeft:"10px",marginRight:"10px",marginTop:"10px"}} >
                                    Page { this.state.inventory_pagination.number}  of  {this.state.inventory_pagination.num_pages}
                                </span>

                            { this.state.inventory_pagination.has_next ? 
                                <React.Fragment> 
                                    <button className="page-link" onClick={this.change_page} value={this.state.inventory_pagination.next_page_number}  >next</button> 
                                    <button className="page-link" onClick={this.change_page} value={this.state.inventory_pagination.num_pages} >last </button>
                                </React.Fragment>

                            : <h1></h1>
                            }
                        </ul>
                    </span>
                </div>     
            </div>
        )
    }
    componentDidMount=()=>{
        this.getInventory("All")
    }
    
    // Send api request for all business inventory matching query
    getInventory=(query,page_num)=>{
        console.log("populate all_inventory state", query)
        // If query is empty get all inventory
        if(!query.trim()){
            query = "ALL"
        }  
        // Send request for invenntory data
        fetch(`${HOST}/business/${business_name}/inventory/${query}/${page_num}`)
         .then(response=>{
             return response.json()
        })
         // Update all_inventory and pagition state with data received
        .then(response=>{
            console.log(response)
            this.setState({
                all_inventory :response[0],
                inventory_pagination:{
                    has_next:             response[1][0].has_next,
                    has_previous:         response[1][0].has_previous,
                    num_pages:             response[1][0].num_pages,
                    number:               response[1][0].number,
                    next_page_number:      response[1][0].next_page_number,
                    previous_page_number:  response[1][0].previous_page_number,
                }

            })
        })
    }
    
    // Request next group of inventory in pagnition page
    change_page = (event) =>{
        this.getInventory(this.state.inventory_query, event.target.value)
    }
    handleChange=(event)=>{
        // Change query state
        if(event.target.name === 'query-inventory'){
            this.setState({
                inventory_query:event.target.value
            })
        }
    }
    handleClick=(event)=>{
        // Get inventory matching query
        if(event.target.name === 'submit-query'){
            this.getInventory(this.state.inventory_query, 1)   
        }
    }

    // Handles how inventory are displayed
    mapInventoryItems =()=>{             
        var all_inventory_mapped = this.state.all_inventory.map(inventory=>{  
            let editing = false  

            if(this.state.edit && inventory.id === this.state.edit ){   
                editing = true   
            }
            return <InventoryItem
                key = {inventory.id}
                inventory = {inventory}
                edit_inventory = {this.edit_inventory}
                editing ={editing}
            />     
        })  

        if (all_inventory_mapped){
            return all_inventory_mapped         
        }
        return (<div className="col-md-12"><h2 className="text-center">No Employees</h2></div>)
    }
    
    // Change inventory to edit
    edit_inventory=(inventory_id)=>{
        this.setState({
            edit:inventory_id
        })
        if(inventory_id === "None"){
            console.log("get_all")
            this.getInventory(this.state.inventory_query,this.state.inventory_pagination.number)
        }
    }
}

// How individual inventory is displayed
class InventoryItem extends React.Component{
    constructor(props){
        super(props)  
        this.state={
            name:this.props.inventory.name,
            description:this.props.inventory.description,
            price:this.props.inventory.price,
            unit:this.props.inventory.unit,
        }  
    }

    render(){
        return(
            <React.Fragment>
                {/* Display inventory edit form or without edit form */}
                {this.props.editing?
                    <div className="container-overlay">
                        <div className='container-center-column overlay-inventory'>
                            <div className="form-box-small">
                                <div className="image" style={{height:"300px",maxHeight:"350px",minHeight:"220px", marginBottom:"2em"}}>
                                    {this.props.inventory.image?
                                        <img src={this.props.inventory.image} style={{objectFit: "fill"}}></img>
                                        :
                                        <div>None Image</div>
                                    }
                                </div>
                                <div className="form-group choose-image">
                                    <label>Change Image</label>
                                    <input className="form-control-file" type="file" id="new_inventory_image"></input>
                                </div>

                                <div className="form-group name">
                                    <label>Name</label>
                                    <input name="inventory-name" type="text" className="form-control" defaultValue={this.props.inventory.name} onChange={this.handleChange}></input>
                                </div>
                                <div className="form-group price">
                                    <label>Price</label>
                                    <input name="inventory-price" type="number" step='.01' className="form-control" defaultValue={this.props.inventory.price} onChange={this.handleChange}></input>
                                </div>
                                <div className="form-group unit">
                                    <label>Unit</label>
                                    <input name="inventory-unit" type="text" className="form-control" defaultValue={this.props.inventory.unit} onChange={this.handleChange}></input>
                                </div>

                                <div className="form-group description">
                                    <label>Description</label>
                                    <textarea name="inventory-description" className="form-control" defaultValue={this.props.inventory.description} onChange={this.handleChange}></textarea>
                                </div>

                                <div className="form-group container-center-row">
                                    <button className="btn btn-success" onClick={this.handleClick} name="save-form" style={{marginRight:"2em",color:"white"}}>SAVE</button>
                                    <button className="btn btn-danger" onClick={this.handleClick} name="delete-form" style={{color:"white"}}>DELETE</button>
                                </div>
                            </div><br></br>
                            <div className="close-form">
                                <button className="btn btn-primary" onClick={this.handleClick} name="close-form">Close</button>
                            </div>
                        </div> 
                    </div>
                :
                    <div className="container-center-column col-md-4" >
                        <div className="index-inventory-item">
                            <div className="image">
                                {this.props.inventory.image?
                                    <img src={this.props.inventory.image}></img>
                                    :
                                    <div>None Image</div>
                                }
                            </div>

                            <div className="name">
                                <h2>        
                                    <a href={this.props.inventory.url_page} >{this.props.inventory.name}</a>
                                </h2>
                            </div>
                            <div className="price">
                                <p>
                                    GHC {this.props.inventory.price}
                                </p>
                            </div>
                            <div className="unit">
                                <p>
                                    / {this.props.inventory.unit}
                                </p>
                            </div>

                            <div className="footer-2">
                                <button className="btn btn-primary" onClick={()=>this.props.edit_inventory(this.props.inventory.id)}>EDIT</button>
                            </div>
                        </div>
                    </div>
                }   
            </React.Fragment>
        ) 
    }

    handleChange=(event)=>{
        // Change state inventory name and wait for change request to be sent  
        if(event.target.name === "inventory-name"){
            this.setState({
                name: event.target.value
            })
        }
        // Change state inventory price and wait for change request to be sent  
        else if(event.target.name === "inventory-price"){
            this.setState({
                price: event.target.value 
            })
        } 
        // Change state inventory unit and wait for change request to be sent  
        else if(event.target.name === "inventory-unit"){
            this.setState({
                unit: event.target.value   
            })  
        } 
        // Change state inventory description and wait for change request to be sent  
        else if(event.target.name === "inventory-description"){
            this.setState({
                description: event.target.value   
            })  
        }   
    }

    handleClick=(event)=>{
        console.log(event.target.value)
        if(event.target.name === "close-form"){
            this.props.edit_inventory(" ")
        }
        else if(event.target.name === "save-form"){
            this.save_changes("SAVE CHANGES")
            
        }
        else if(event.target.name === "delete-form"){
            this.save_changes("DELETE")
            
        }
    }

    save_changes=(method)=>{
        // Request deletion of inventory
        if(confirm(`Do you want to ${method} inventory`)){
            if(method === "DELETE"){
                fetch(`${HOST}/business/${business_name}/inventory_management/`,{
                        method:'DELETE',
                        
                        headers: {
                            "X-CSRFToken": getCookie("csrftoken")
                        },
                        body:JSON.stringify({
                            "id":this.props.inventory.id
                        }),
                    })
            }
            // Request save of changes to inventory
            else{

                let new_image = document.getElementById("new_inventory_image")
                const form_data = new FormData()

                if(new_image.files[0]){
                    form_data.append("new_image",new_image.files[0])
                }else{
                    console.log("no new image chosen")
                }

                form_data.append("id",this.props.inventory.id)
                form_data.append("name",this.state.name)
                form_data.append("description",this.state.description)
                form_data.append("price",this.state.price)
                form_data.append("unit",this.state.unit)

                // console.log(form_data.get('name'))
                
                fetch(`${HOST}/business/${business_name}/inventory_management/`,{
                    method:'POST',
                    mode:'same-origin',
                    headers: {
                        "Accept":"application/json",
                        "X-Requested-With":'XMLHttpRequest',
                        "X-CSRFToken": getCookie("csrftoken")
                    },
                    body:form_data,
                })
            }
            this.props.edit_inventory("None")
        }
    }
}


ReactDOM.render(<InventoryManagement/>,document.querySelector('#show_inventory'));
// console.log(business_name)


