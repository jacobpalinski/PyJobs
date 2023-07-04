import './App.css';
import {useState} from 'react';

function App() {
	const [isSignUpActive, setIsSignUpActive] = useState(false);

	const handleSignUpClick = () => {
		setIsSignUpActive(true);
	}

	const handleSignInClick = () => {
		setIsSignUpActive(false);
	};

  return (
    <div>
<div className="heading">
	<img src="/pythonlogo.png" alt="Logo"/>
	<h1>PyJobs</h1>
</div>
<div className={`container ${isSignUpActive ? 'right-panel-active' : ''}`}>
	<div className="form-container sign-up-container">
		<form action="#">
			<h1>Create Account</h1>
			<input type="text" placeholder="Username" />
			<input type="password" placeholder="Password" />
			<button>Sign Up</button>
		</form>
	</div>
	<div className="form-container sign-in-container">
		<form action="#">
			<h1>Sign in</h1>
			<input type="text" placeholder="Username"/>
			<input type="password" placeholder="Password" />
			<button>Sign In</button>
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
