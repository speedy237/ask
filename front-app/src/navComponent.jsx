import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';

function NavComponent() {
  return (
    <>
     
      <Navbar bg="primary" data-bs-theme="dark">
        <Container>
          <Navbar.Brand href="#home">Job Application Aubay</Navbar.Brand>
          <Nav className="me-auto">
            <Nav.Link href="#home">Jobs</Nav.Link>
            <Nav.Link href="#features">Candidates</Nav.Link>
            <Nav.Link href="#pricing">Dashboard</Nav.Link>
            <Nav.Link href="#pricing">Report</Nav.Link>
          </Nav>
        </Container>
      </Navbar>

    </>
  );
}

export default NavComponent;