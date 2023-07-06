import '../css/loginSignUp.css';
import {useState, useEffect} from 'react';
/* import {useNavigate} from 'react-router-dom'; (redirection in individual component files)
import {BrowserRouter, Routes, Route, Link} from 'react-router-dom' in App.js (for defining routes in return)
import LoginSignUp from "./path" */

export default function LoginSignUp() {
	const initialValues = { username: "", password: ""}
	const [signInFormValues, setSignInFormValues] = useState(initialValues);
	const [signUpFormValues, setSignUpFormValues] = useState(initialValues);
	const [signInFormErrors, setSignInFormErrors] = useState({});
	const [signUpFormErrors, setSignUpFormErrors] = useState({});
	const [signInSubmit, setSignInSubmit] = useState(false);
	const [signUpSubmit, setSignUpSubmit] = useState(false);
	const [login, setLogin] = useState(true);
	const [registered, setRegistered] = useState(false);
	const [isSignUpActive, setIsSignUpActive] = useState(false);

	// const navigate = useNavigate();

	const handleSignInChange = (e) => {
		const {name, value} = e.target;
		setSignInFormValues({...signInFormValues, [name]: value});
		console.log(signInFormValues);
	};

	const handleSignUpChange = (e) => {
		const {name, value} = e.target;
		setSignUpFormValues({...signUpFormValues, [name]: value});
		console.log(signUpFormValues);
	};

	const signIn = (e) => {
		e.preventDefault();
		setSignInFormErrors(validateSignIn(signInFormValues));
		setSignInSubmit(true);
	};

	const signUp = (e) => {
		e.preventDefault();
		setSignUpFormErrors(validateSignUp(signUpFormValues));
		setSignUpSubmit(true);
	}

	useEffect(() => {
		console.log(signInFormErrors);
		if(Object.keys(signInFormErrors).length === 0 && signInSubmit) {
			console.log(signInFormValues);
			const fetchLogin = async () => {
				try {
					const response = await fetch('http://127.0.0.1:5000/job_data/user/login',{
						method: 'POST',
						headers: {
							'Content-Type': 'application/json'
						},
						body: JSON.stringify(signInFormValues)
					});
					if (response.ok) {
						const data = await response.json();
						console.log(data);
						localStorage.setItem('auth_token', data.auth_token);
						setSignInSubmit(false);
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
	}, [signInFormErrors, signInFormValues, signInSubmit]);

	useEffect(() => {
		console.log(signUpFormErrors);
		if (Object.keys(signUpFormErrors).length === 0 && signUpSubmit) {
			console.log(signUpFormValues);
			const fetchSignUp = async () => {
				try {
					const response = await fetch('http://127.0.0.1:5000/job_data/user',{
						method: 'POST',
						headers: {
							'Content-Type': 'application/json'
						},
						body: JSON.stringify(signUpFormValues)
					});
					if (response.ok) {
						setRegistered(true);
						console.log('Successful Sign Up');
					} else {
						const errorData = await response.json();
						console.log(errorData);
					}
	
				} catch (error) {
					console.error('Error during login:', error);
				}
			};
			fetchSignUp();
		}
	}, [signUpFormErrors, signUpFormValues, signUpSubmit])

	const validateSignIn = (values) => {
		const errors = {};
		if (!values.username) {
			errors.username = "Username is required";
		};
		if (!values.password) {
			errors.password = "Password is required";
		};
		return errors;
	};

	const validateSignUp = (values) => {
		const errors = {};
		const checkDigit = /\d/;
		const checkUppercaseLetter = /[A-Z]/;
		const checkLowercaseLetter = /[a-z]/;
		const checkSpecialCharacters = /[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]/; 

		if (!values.username) {
			errors.username = "Username is required";
		} else if (values.username.length < 5) {
			errors.username = "Username must have at least 5 characters";
		} else if (!checkUppercaseLetter.test(values.username) && !checkLowercaseLetter.test(values.username)) {
			errors.username = "Username must contain at least 1 letter";
		} else if (!checkDigit.test(values.username)){
			errors.username = "Username must contain at least 1 digit";
		}

		if (!values.password) {
			errors.password = "Password is required";
		} else if (values.password.length < 8) {
			errors.password = "Password must have at least 8 characters";
		} else if (values.password.length > 32) {
			errors.password = "Password must be less than 32 characters";
		} else if (!checkUppercaseLetter.test(values.password)) {
			errors.password = "Password must contain at least 1 uppercase letter";
		} else if (!checkLowercaseLetter.test(values.password)) {
			errors.password = "Password must contain at least 1 lowercase letter";
		} else if (!checkDigit.test(values.password)){
			errors.password = "Password must contain at least 1 digit";
		} else if (!checkSpecialCharacters.test(values.password)) {
			errors.password = "Password must contain at least 1 special character";
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
		<form onSubmit = {signUp}>
			<h1>Create Account</h1>
			<input type="text" name="username" value={signUpFormValues.username} onChange={handleSignUpChange} placeholder="Username" />
			<p>{signUpFormErrors.username}</p>
			<input type="password" name="password" value={signUpFormValues.password} onChange={handleSignUpChange} placeholder="Password" />
			<p>{signUpFormErrors.password}</p>
			<button>Sign Up</button>
			{registered && <p>Sign Up Successful. Login with Credentials</p>}
		</form>
	</div>
	<div className="form-container sign-in-container">
		<form onSubmit = {signIn}>
			<h1>Sign in</h1>
			<input type="text" name="username" value={signInFormValues.username} onChange={handleSignInChange} placeholder="Username"/>
			<p>{signInFormErrors.username}</p>
			<input type="password" name="password" value={signInFormValues.password} onChange={handleSignInChange} placeholder="Password" />
			<p>{signInFormErrors.password}</p>
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
