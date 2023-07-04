import './App.css';
import {useState, useEffect} from 'react';
/* import {useNavigate} from 'react-router-dom'; (redirection in individual component files)
import {BrowserRouter, Routes, Route, Link} from 'react-router-dom' in App.js (for defining routes in return)
import LoginSignUp from "./path" */

function App() {
	const initialValues = { username: "", password: ""}
	const [formValues, setFormValues] = useState(initialValues);
	const [formErrors, setFormErrors] = useState({});
	const [isSubmit, setIsSubmit] = useState(false);
	const [login, setLogin] = useState(true);
	const [isSignUpActive, setIsSignUpActive] = useState(false);

	// const navigate = useNavigate();

	const handleChange = (e) => {
		const {name, value} = e.target;
		setFormValues({...formValues, [name]: value});
		console.log(formValues);
	};

	const handleSubmit = (e) => {
		e.preventDefault();
		setFormErrors(validate(formValues));
		setIsSubmit(true);
	};

	useEffect(() => {
		console.log(formErrors);
		if(Object.keys(formErrors).length === 0 && isSubmit) {
			console.log(formValues);
			const fetchLogin = async () => {
				try {
					const response = await fetch('http://127.0.0.1:5000/job_data/user/login',{
						method: 'POST',
						headers: {
							'Content-Type': 'application/json'
						},
						body: JSON.stringify(formValues)
					});
					if (response.ok) {
						console.log('Successful login');
						// navigate()
					} else {
						setLogin(false);
						const errorData = await response.json();
						console.log(errorData);
					}
	
				} catch (error) {
					console.error('Error during login:', error);
				}
			};
			fetchLogin();
		}
	}, [formErrors, formValues, isSubmit])

	const validate = (values) => {
		const errors = {};
		if (!values.username) {
			errors.username = "Username is required";
		};
		if (!values.password) {
			errors.password = "Password is required";
		}
		return errors;
	}

	const handleSignUpClick = () => {
		setIsSignUpActive(true);
	};

	const handleSignInClick = () => {
		setIsSignUpActive(false);
	};

	/* After first <div> tag (after code has been moved to component javascript file) add the following code:
	<BrowserRouter>
	 <Routes>
	  <Route path = "(desired path) eg. /jobs" element = {component eg. LoginSignUp />} />
	 </Routes>
	</BrowserRouter>
	*/
  return (
    <div>
<div className="heading">
	<img src="/pythonlogo.png" alt="Logo"/>
	<h1>PyJobs</h1>
</div>
<div className={`container ${isSignUpActive ? 'right-panel-active' : ''}`}>
	<div className="form-container sign-up-container">
		<form onSubmit = {handleSubmit}>
			<h1>Create Account</h1>
			<input type="text" name="username" value={formValues.username} onChange={handleChange} placeholder="Username" />
			<p>{formErrors.username}</p>
			<input type="password" name="password" value={formValues.password} onChange={handleChange} placeholder="Password" />
			<p>{formErrors.password}</p>
			<button>Sign Up</button>
		</form>
	</div>
	<div className="form-container sign-in-container">
		<form onSubmit = {handleSubmit}>
			<h1>Sign in</h1>
			<input type="text" name="username" value={formValues.username} onChange={handleChange} placeholder="Username"/>
			<p>{formErrors.username}</p>
			<input type="password" name="password" value={formValues.password} onChange={handleChange} placeholder="Password" />
			<p>{formErrors.password}</p>
			<button>Sign In</button>
			{!login && <p>Invalid Credentials. Try Again</p>}
		</form>
	</div>
	<div className="overlay-container">
		<div className="overlay">
			<div className="overlay-panel overlay-left">
				<h1>Welcome Back!</h1>
				<p>Simply login and start searching</p>
				<button className="ghost" onClick={handleSignInClick}>Sign In</button>
			</div>
			<div className="overlay-panel overlay-right">
				<h1>Hello, Python Enthusiast!</h1>
				<p>Enter your details and start looking for a job thats right for you!</p>
				<button className="ghost" onClick={handleSignUpClick}>Sign Up</button>
			</div>
		</div>
	</div>
</div>
    </div>
  );
}

export default App;
