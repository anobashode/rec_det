import React, { Component } from 'react';
import './Main.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faShopLock } from '@fortawesome/free-solid-svg-icons'
// import { Link } from 'react-router-dom'
import { Navbar, Nav, Container } from 'react-bootstrap';
import User from './User';
import Deliver from './Deliver';
class NavBar extends Component {

  constructor(props) {
    super(props);
    this.state = {
        flag: true
    };
}
renderUserPage = () => {
  this.setState({flag:true});
}

renderDeliveryPage = () => {
  this.setState({flag:false});
}

    render() {
        return (
          <div>
            <Navbar bg="light" expand="lg">
                <Navbar.Brand href="#home">
                <Nav.Link className="nav-link active">
                  <FontAwesomeIcon icon={faShopLock}  color="#0275d8" width="30" height="30" alt="" />
                         {'  '}Future Delivery Service
                  </Nav.Link>
                  </Navbar.Brand>
              <Container>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                  <Nav className="me-auto">
                  <Nav.Link className="nav-link" onClick = {this.renderUserPage}>Add Consignment</Nav.Link>
                  <Nav.Link className="nav-link" onClick = {this.renderDeliveryPage}>Deliver Consignment</Nav.Link>
                  </Nav>
                </Navbar.Collapse>
              </Container>
            </Navbar>
            {this.state.flag ?
              <User />
            :
              <Deliver />
            }
            </div>
        );
    }
}
export default NavBar;