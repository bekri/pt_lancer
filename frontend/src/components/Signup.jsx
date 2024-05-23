import React, {useState} from 'react'

const Signup = () => {

    return (
      <div>
        <div className='form-container'>
          <div className='wrapper'>
            <h2>Create Account</h2>
            <form action="">
            <div className='form-group'>
                 <label htmlFor="">Email Address:</label>
                 <input type="text"
                  className='email-form'  
                  name="email" />
            </div>
            <div className='form-group'>
                 <label htmlFor="">First Name:</label>
                 <input type="text"
                  className='email-form'  
                  name="first_name" />
            </div>
            <div className='form-group'>
                 <label htmlFor="">Last Name:</label>
                 <input type="text"
                  className='email-form'  
                  name="last_name" />
            </div>

            <div className='form-group'>
                 <label htmlFor="">Password:</label>
                 <input type="password"
                  className='email-form'  
                  name="password" />
            </div>

            <div className='form-group'>
                 <label htmlFor="">Confirm Password:</label>
                 <input type="password"
                  className='email-form'  
                  name="password" />
            </div>

            <div className='form-group'>
                 <label htmlFor="">Role:</label>
                 <input type="field"
                  className='email-form'  
                  name="role" />
            </div>

            <input type="submit" value="submit" className="submitButton" />
            </form>
          </div>
        </div>
      </div>
    )
}