import {useEffect, useState} from 'react';
import '../css/jobs.css';
import Select from "react-select";

export default function Jobs() {
    let [data, setData] = useState([]);
    const [location, setLocation] = useState("");
    const [company, setCompany] = useState("");
    const [group, setGroup] = useState("");
    const [datePosted, setDatePosted] = useState(0);
    const [jobTitle, setJobTitle] = useState("");
    const [selectedDatabases, setSelectedDatabases] = useState([]);
    const [selectedCloudProviders, setSelectedCloudProviders] = useState([]);
    const databases = [
        {value: "MySQL", label: "MySQL"},
        {value: "PostgreSQL", label: "PostgreSQL"},
        {value: "SQLite", label: "SQLite"},
        {value: "MongoDB", label: "MongoDB"},
        {value: "MS SQL", label: "MS SQL"},
        {value: "SQL Server", label: "SQL Server"},
        {value: "Maria DB", label: "Maria DB"},
        {value: "Firebase", label: "Firebase"},
        {value: "ElasticSearch", label: "ElasticSearch"},
        {value: "Oracle", label: "Oracle"},
        {value: "DynamoDB", label: "DynamoDB"}
    ];
    const cloudProviders = [
        {value: "Amazon Web Services", label: "Amazon Web Services"},
        {value: "AWS", label: "AWS"},
        {value: "Azure", label: "Azure"},
        {value: "Google Cloud", label: "Google Cloud"},
        {value: "GCP", label: "GCP"}
    ];

    console.log(data);

    //custom data
    useEffect(() => {
        const fetchjobData = async () => {
            // Base URL
            let url = 'http://127.0.0.1:5000/job_data/jobData';
            // Query parameters based on selected values
            const queryParams = [];

            if (location) {
                queryParams.push(`location=${location}`);
            }

            if (company) {
                queryParams.push(`company=${company}`);
            }

            if (group) {
                queryParams.push(`group=${group}`);
            }

            if (datePosted) {
                queryParams.push(`days_old=${datePosted}`);
            }

            if (jobTitle) {
                queryParams.push(`jobTitle=${jobTitle}`);
            }

            if (selectedDatabases) {
                selectedDatabases.forEach( (database) => {
                    queryParams.push(`database=${database}`);
                })
            }

            if (selectedCloudProviders) {
                selectedCloudProviders.forEach( (provider) => {
                    queryParams.push(`cloud=${provider}`);
                })
            }

            console.log(queryParams);

            if (queryParams.length > 0) {
                url += `?${queryParams.join('&')}`;
            }

            try {
                const response = await fetch(url, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                const data = await response.json();
                setData(data);
            } catch (error) {
                console.error('Error retrieving data', error);
            }
        };
        fetchjobData();
    }, [location, company, group, datePosted, jobTitle, selectedDatabases, selectedCloudProviders]);

    // select onchange function getting option selected value and save inside state variable
    function handleLocationChange (e) {
        setLocation(e.target.value);
    };

    function handleCompanyChange (e) {
        setCompany(e.target.value);
    }

    function handleGroupChange (e) {
        setGroup(e.target.value);
    }

    function handleDatePosted (e) {
        setDatePosted(e.target.value);
    }

    function handleJobTitle (e) {
        setJobTitle(e.target.value);
    }

    function handleSelectedDatabases (e) {
        setSelectedDatabases(e.map(database => database.value));
    }

    function handleSelectedCloudProviders (e) {
        setSelectedCloudProviders(e.map(provider => provider.value));
    }

    //hooks calls after rendering select state
    /*useEffect(() => {
        // Doing filtration based on location
        const jobData = initialData.filter(jobData => jobData.location === location 
            && jobData.company === company 
            && jobData.group === group);
        setData(jobData);
    }, [location, company, group, datePosted])*/

    return (
        <div>
            <div className="jobs-container">
                <h1 className="jobs-header">Jobs</h1>
                <div className="filters">
                    <div className="date-posted">
                        <label className="form-label">Date Posted</label>
                            <select id="date-posted" onChange={handleDatePosted} className="form-select">
                                <option value={1}>&lt; 1 day</option>
                                <option value="Graduate Software Developer (Python)">Graduate Software Developer (Python)</option>
                            </select>
                    </div>
                    <div className="location">
                        <label className="form-label">Location</label>
                            <select id="city" onChange={handleLocationChange} className="form-select">
                                <option value="Glasgow">Glasgow</option>
                                <option value="Barcelona">Barcelona</option>
                                <option value="Berlin">Berlin</option>
                            </select>
                    </div>
                    <div className="company">
                        <label className="form-label">Company</label>
                        <select id="company" onChange={handleCompanyChange} className="form-select">
                            <option value="Reloadly">Reloadly</option>
                            <option value="ClickJobs.io">ClickJobs.io</option>
                        </select>
                    </div>
                    <div className="group">
                        <label className="form-label">Group</label>
                        <select id="group" onChange={handleGroupChange} className="form-select">
                            <option value="Software Engineering / Development">Software Engineering / Development</option>
                            <option value="Data Science / Engineering">Data Science / Engineering</option>
                        </select>
                    </div>
                    <div className="databases">
                        <label className="form-label">Databases</label>
                        <Select options={databases} onChange={handleSelectedDatabases} isMulti/>
                    </div>
                    <div className="cloud-providers">
                        <label className="form-label">Cloud Providers</label>
                        <Select options={cloudProviders} onChange={handleSelectedCloudProviders} isMulti/>
                    </div>
                    <div className="jobtitle">
                        <label className="form-label">Job Title</label>
                        <input type="text" name="search" onChange={handleJobTitle} placeholder="Job Title" />
                    </div>
                </div>
                {data.length !== 0 ? (<div className="table-container">
                <table className="table">
                    <thead>
                        <tr>
                            <th scope="col">Date Posted</th>
                            <th scope="col">Location</th>
                            <th scope="col">Company</th>
                            <th scope="col">Group</th>
                            <th scope="col">Job Title</th>
                            <th scope="col">Databases</th>
                            <th scope="col">Cloud Providers</th>
                            <th scope="col">Link</th>
                        </tr>
                    </thead>
                    <tbody>
                        { // calling the state variable to filter data inside table
                        data.map(function({datePosted,location,company,group,jobTitle,databases,cloudProviders,link})
                        {
                            return (
                                <tr>
                                    <td>{datePosted}</td>
                                    <td>{location}</td>
                                    <td>{company}</td>
                                    <td>{group}</td>
                                    <td>{jobTitle}</td>
                                    <td>{databases.join(', ')}</td>
                                    <td>{cloudProviders.join(', ')}</td>
                                    <td><a href={link}>{link}</a></td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
            </div> ) : (<p>No jobs exist for given filters</p>)}
        </div>
    </div>
    );
}