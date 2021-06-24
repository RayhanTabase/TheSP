
const HOST = "http://127.0.0.1:8000"

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

// General layout of create invoice page
class SalesInvoice extends React.Component{
    constructor(props){
        super(props)
        this.state ={
            all_inventory:[],
            invoice_items:[],
            grand_total : 0,
            add_new_item:false,

            customer_name:"",
            customer_contact:"",
            customer_username:"",


            inventory_pagination:{
                has_next:false,
                has_previous:false,
                num_pages:"",
                number:"",
                next_page_number:"",
                previous_page_number:""

            },

            inventory_query:"",
            error_message:"",
            discount_amount:0
        }
    }
      
    render(){
        const all_inventory_listed = this.mapInventoryItems()
        const invoice_items_listed = this.mapInvoiceItems()
        return (
            <div className="container-fluid" >
                {/* Show all inventory of business that can be added to invoice */}
                {this.state.add_new_item? 
                    <div className="container-overlay">
                        <div className="container-center-column">
                            <div className="overlay-inventory">
                        
                                <div className="form-group search-box"> 
                                    <input className="form-control" name="query-inventory" type="text" onChange={this.handleChange} placeholder="Search"/>
                                </div>   
                                <table className="table table-dark table-bordered table-striped">
                                    <thead >
                                    <tr>
                                        <th scope="col">Name</th>
                                        <th scope="col">Price</th>
                                        <th scope="col">#</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                        {all_inventory_listed}
                                    </tbody>
                                </table>
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
                                <div className="container-center-column lone-btn">
                                    <button className="btn btn-primary" name="close_inventory" onClick={this.handleClick}>Close</button>          
                                </div>
                            </div>
                        </div>
                    </div>
                :    
                    <div className="container-center-column lone-btn">
                        <button className="btn btn-primary btn-lg" name="open_inventory" onClick={this.handleClick}>Add Item</button>
                    </div>    
                }
      
                {/* Show invoice list */}
                <div className="table-responsive invoice-items">
                    <table className="table table-bordered table-hover">
                        <thead className="thead-dark">
                            <tr>
                                <th scope="col">Name</th>
                                <th scope="col">Price</th>
                                <th scope="col">Units</th>
                                <th scope="col">Total</th>
                                <th scope="col">Add</th>
                                <th scope="col">Reduce</th>
                            </tr>
                        </thead>
                        <tbody>
                            {invoice_items_listed}
                        </tbody>
                    </table>
                </div>
                {/* Show total of all invoice items */}
                <div className="text-center">
                    <h2 >( {this.state.discount_amount} ) </h2>
                    <h2 style={{textDecoration: "double underline",}} >TOTAL = {this.state.grand_total - this.state.discount_amount} </h2>
                </div><br></br><br></br>

                {/* Add a discount amount  */}
                <div className="discount_input">
                    <input type="number" step='.01' min="1" className="form-control"  placeholder="Discount Amount" name="discount_amount" onChange={this.handleChange}></input>
                </div>
                
                {/* Add customer details */}
                <div>
                    <form>
                        <input type="text" hidden required></input>

                        <div id="customer_username_input" className="form-group">
                            <label className="invalid_username"></label>
                            <input className="form-control" name="customer_username" onChange={this.check_customer_username} placeholder="Customer username"></input>
                        </div>

                        <div id="customer_details_input">
                            
                            <div className="form-group">
                                <input className="form-control" id="customer_name" placeholder="Customer Name" onChange={this.handleChange} required></input>      
                            </div>
                            <div className="form-group">  
                                <input className="form-control" type="text" id="customer_contact" placeholder="Customer Contact" onChange={this.handleChange} required></input>
                            </div>

                        </div>
                        {this.state.error_message?
                            <div className="box-center">
                                <h2>{this.state.error_message}</h2>
                            </div>
                        :
                            false
                        }

                        <div className = "container-center-column lone-btn">
                            <button className="btn btn-success btn-lg" onClick={this.processInvoice}>Process and Proceed to Payment</button>
                        </div>
                    </form>
                </div>
            </div>          
        )
    }
    
    // Check validity of customer username to process invoice
    check_customer_username=(event)=>{
        event.persist();
        let invalid_box = document.querySelector(".invalid_username")
        let customer_name_box = document.querySelector("#customer_name")
        let customer_contact_box = document.querySelector("#customer_contact")
        customer_name_box.value = ""
        customer_contact_box.value = ""

        invalid_box.innerHTML = ""

        fetch(`${HOST}/check_username/${event.target.value}/`)
        .then(response=>{
            if(response.status === 200){
                return response.json()
            }
        })
        .then(response=>{
            if(response){
                this.setState({
                    customer_name : response.name,
                    customer_contact: response.contact,
                    customer_username : event.target.value
                })
                customer_name_box.value = response.name
                customer_contact_box.value = "+" + response.contact    
            }
            else{
                this.setState({
                    customer_name : "",
                    customer_contact: "",
                    customer_username : ""
                })
                invalid_box.innerHTML = "Invalid Username"
            }
        })
    }


    change_page = (event) =>{
        this.getInventory(this.state.inventory_query, event.target.value)
    }

    componentDidMount=()=>{
        this.getInventory("All")
    }

    handleClick=(event)=>{
        if(event.target.name === 'open_inventory'){
            this.setState({
                add_new_item:true
            })
        }
        else if(event.target.name === 'close_inventory'){
            this.setState({
                add_new_item:false
            })
        }
    }

    handleChange=(event)=>{
        if(event.target.name === 'query-inventory'){
            this.setState({
                inventory_query:event.target.value
            })
            this.getInventory(event.target.value,1)
        }
        else if(event.target.id === "customer_name"){
            this.setState({
                customer_name : event.target.value,
            })
        }
        else if(event.target.id === "customer_contact"){
            this.setState({  
                customer_contact: event.target.value,
            })
        }
        else if(event.target.name === "discount_amount"){
            var amount = parseFloat(event.target.value)
            if(this.state.grand_total <= event.target.value ) {
                amount = 0
                event.target.value = 0
            } 
            this.setState({  
                discount_amount: amount,
            })  
        }   
    }

    // Query inventory items that can be added to invoice
    getInventory=(query,page_num)=>{
        console.log("populate all_inventory state", query)
        if(!query.trim()){
            query = "ALL"
        }  
        // Send request for invenntory data
        fetch(`${HOST}/business/${business_name}/inventory/${query}/${page_num}`)
         .then(response=>{
             return response.json()
        })
         // Update all_inventory state with data received
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
    // Handle how inventory are displayed
    mapInventoryItems =()=>{         
        var all_inventory_mapped = this.state.all_inventory.map(inventory=>{ 
            var added = false
            this.state.invoice_items.forEach(item=>{
                if(inventory.name === item.name){
                    added = true
                }
            })  
            return <InventoryItem
                    key = {inventory.id}
                    inventory = {inventory}
                    add_to_invoice = {this.add_to_invoice}
                    added = {added}
                />  
        })  
        return all_inventory_mapped         
    }
    
    // How items in invoice are displayed
    mapInvoiceItems =()=>{         
        var items_mapped = this.state.invoice_items.map(inventory=>{  
            return <InvoiceItem
                key = {inventory.id}
                inventory = {inventory}
                add_to_invoice = {this.add_to_invoice}
                reduce_invoice = {this.reduce_invoice}
            />     
        })  
        return items_mapped        
    }
    
    // Add item to invoice
    add_to_invoice=(item, quantity)=> {
        console.log("add to cart",item.name,quantity)
        var new_item = true
        // If item in invoice increase quantity
        if(this.state.invoice_items){
            this.state.invoice_items.forEach(element=>{
                if(element.id === item.id){
                    console.log("update quantity")
                    element.quantity = parseInt(element.quantity) + parseInt(quantity)
                    element.total = element.price * element.quantity
                    new_item = false
                }
            })
        }

        if(new_item){
            console.log("add to cart") 
            item.quantity = quantity
            item.total = item.price * quantity
            this.state.invoice_items.push(item)  
        }
        
        this.grand_total()
    }
    
    // Remove item or quantity from invoice
    reduce_invoice =(item)=> {
        console.log("reduce cart",item.name)    
        this.state.invoice_items.forEach(element=>{
            if(element.id === item.id){
                console.log("update quantity")
                element.quantity = element.quantity - 1
                if (element.quantity === 0){
                    var index = this.state.invoice_items.indexOf(element)
                    this.state.invoice_items.splice(index,1)
                }           
            }
        })
        this.grand_total()
    }
    
    // Calculate all total
    grand_total =()=>{
        var grand_total = 0
        this.state.invoice_items.forEach(element=>{
            grand_total =  grand_total + (element.price * element.quantity)
        })

        // Check discount amount if less than grand total then set to 0
        if(this.state.discount_amount <= grand_total ) {
            this.setState({  
                discount_amount: 0,
            })
        }

        this.setState({
            grand_total:grand_total,
        })
        console.log(this.state.discount_amount)
    }

    processInvoice =()=>{
        console.log("processing invoice, saving and redirect to payment",this.state.customer_username)
        console.log(this.state.invoice_items)
        // Send data heading(either employee created  true or false) business name inventory name and quantity 
        if (confirm('Are you sure you want to process invoice?')){
            // Process Invoice
            if(this.state.invoice_items.length > 0){
                if(this.state.customer_username || this.state.customer_name && this.state.customer_contact ){
                    fetch(`${HOST}/business/${business_name}/invoices/create/`,{
                        method:'POST',
                        body: JSON.stringify({
                            'employee_created': true,
                            'invoice_items': this.state.invoice_items,
                            'customer_username': this.state.customer_username,
                            'customer_name': this.state.customer_name,
                            'customer_contact':this.state.customer_contact,
                            'discount': this.state.discount_amount
                            
                        }),
                        headers: {
                            "X-CSRFToken": getCookie("csrftoken")
                        }
                    })
                    .then(response=>{
                        console.log(response)
                        if(response.status === 200){
                            return response.json()
                        }else{
                            alert("not saved")
                        }
                    })
                    .then(response=>{
                        if(response){
                            let invoice_id = response['invoice_id']
                            window.location.assign(`${HOST}/business/${business_name}/manage_invoice/${invoice_id}/`)
                        }
                    })
                }
                else{
                    alert("you must provide customer details")
                }
            }else{
                alert("invoice is empty")
            }
        }else{
            // Do nothing!
            console.log('cancelled');
        }
    }
}

// How Inventory items are displayed, to be added to invoice
class InventoryItem extends React.Component{
    constructor(props){
        super(props)  
        this.state={
            quantity : 1
        }  
    }

    render(){
        return(
            <tr>
                <th style={{textTransform:"capitalize"}} scope="row">{this.props.inventory.name}</th>
                <td>{this.props.inventory.price}</td>
                
                <td> 
                    {this.props.added?
                            false
                        :
                            <button className="btn btn-success btn-small"  onClick={()=>this.props.add_to_invoice(this.props.inventory,this.state.quantity)}   required ={this.props.added} >ADD</button>    
                        }
                 </td>
            </tr>
        )
    }

    handleChange=(event)=>{
        if(event.target.name === "quantity"){
            this.setState({
                quantity:event.target.value
            })
        }
    }
}

class InvoiceItem extends React.Component{
    constructor(props){
        super(props)
        this.state={

        }     
    }
    
    render(){
        return(
            <React.Fragment>
                <tr>
                    <th style={{textTransform:"capitalize"}} scope="row">{this.props.inventory.name}</th>
                    <td >{this.props.inventory.price} </td>
                    <td>{this.props.inventory.quantity} /{this.props.inventory.unit}(s)</td>
                    <td>{this.props.inventory.total} </td>
                    <td>
                        <button className="btn btn-success add-btn" onClick={()=>this.props.add_to_invoice(this.props.inventory,1)} >+</button>   
                    </td>
                    <td>
                        <button className="btn btn-danger reduce-btn " onClick={()=>this.props.reduce_invoice(this.props.inventory)} >-</button> 
                    </td>
                </tr>
            </React.Fragment>
        )
    }
}


ReactDOM.render(<SalesInvoice />,document.querySelector('#body'));   
// console.log(business_name)

