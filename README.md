This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.<br />
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.<br />
You will also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.<br />
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.<br />
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.<br />
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

If you aren’t satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (Webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: https://facebook.github.io/create-react-app/docs/code-splitting

### Analyzing the Bundle Size

This section has moved here: https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size

### Making a Progressive Web App

This section has moved here: https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app

### Advanced Configuration

This section has moved here: https://facebook.github.io/create-react-app/docs/advanced-configuration

### Deployment

This section has moved here: https://facebook.github.io/create-react-app/docs/deployment

### `npm run build` fails to minify

This section has moved here: https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify

## Git Installation For Your Editors.
1. Download git plugin from git official website (https://git-scm.com/download/win). (based on Win version 32/64 bit)
2. Run the git application, Select Next for all the pop-ups and click Finish.
3. Install the git application.
4. You either use git bash/git GUI/VScode cmd prompt for git command line processing.
5. Configure your email and user to your git account (say github) using following command line args,
   - git config --global user.email "registered email id"
   - git config --global user.name "registered username"

## Python code process flow.
1. Install python (3.7) (Whole Package is recommended: Anaconda 5.3.0 and above)
2. Set OS path for python, pip and conda with their respective paths in package.
3. Create a separate virtual environment using the below command.
   - python -m venv (virtual-env-name)
4. Now Activate the virtual environment using the below command,
   - <venv-path>\Scripts\activate

## Note: Follow the below procedure only if you are not able to install python packages either Anaconda - pip or conda. 
## Anaconda Package has almost all modules in it and very reliable to use.
## Python Application packages. (I Have zipped required python packages for this app, in case you face any issues.)
For your reference, You find the list of zipped packges under the 'python-packages-requirement' directory.
How To Install Package Manually?
1. Unzip/extract the python zipped packages in your local.
2. Move the unzip package folder to your venv directory in path as follows,
   -  path: <your-local-directory>\<venv-name>\Lib\site-packages\
   -  Ex: E:\Sabs Learning\resource_integrate\shift_plan\Lib\site-packages\
3. Now Restart your editor and try running the modules.