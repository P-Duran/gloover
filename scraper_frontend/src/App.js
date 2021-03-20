import './App.css';
import { Dashboard } from './pages/Dashboard/Dashboard';
import { GlobalContextProvider } from 'context/GlobalContext'
import Drawer from '@material-ui/core/Drawer';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import { ListItemText, makeStyles } from '@material-ui/core';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect,
  withRouter
} from "react-router-dom";
import { HomeRounded, PostAddRounded } from '@material-ui/icons';
import { useEffect, useState } from 'react';
import { JobCreation } from 'pages/Creation/JobCreation';
import { DASHBOARD_PATH } from 'utils/routeUtils';
import { JOB_CREATION_PATH } from 'utils/routeUtils';

const drawerWidth = 240;

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
  },
  appBar: {
    width: `calc(100% - ${drawerWidth}px)`,
    marginLeft: drawerWidth,
  },
  drawer: {
    width: drawerWidth,
    flexShrink: 0,
  },
  drawerPaper: {
    width: drawerWidth,
  },
  // necessary for content to be below app bar
  toolbar: theme.mixins.toolbar,
  content: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.default,
    padding: theme.spacing(3),
  },
  listItem: {
    backgroundColor: 'transparent',
    '&.Mui-selected': {
      backgroundColor: '#ebf9f1',
      color: "#229A16"
    }

  }
}));
const LateralMenu = withRouter(({ menuItems, classes, history }) => {
  const [selectedPath, setSelectedPath] = useState(history.location.pathname)
  useEffect(() => {
    setSelectedPath(history.location.pathname)
  }, [history.location.pathname]);

  return <List component="nav">
    {menuItems.map(item => (
      <CustomLink
        key={item.name}
        button
        name={item.name}
        route={item.route}
        onClick={() => setSelectedPath(item.route)}
        selected={item.route === selectedPath}
        classes={classes.listItem}>
        <ListItemIcon style={{ color: "#229A16" }}>{item.icon}</ListItemIcon>
        <ListItemText primary={item.name} />
      </CustomLink>
    ))}
  </List>
})
const CustomLink = withRouter(({ history, selected, route, classes, onClick, children }) => (
  <ListItem
    button
    selected={selected}
    className={classes}
    onClick={() => { history.push(route); onClick(); }}
  >
    {children}

  </ListItem>
))
const menuItems = [{ "name": "Dashboard", "route": DASHBOARD_PATH, "icon": <HomeRounded /> }, { "name": "Create Job", "route": JOB_CREATION_PATH, "icon": <PostAddRounded /> }]
function App() {
  const classes = useStyles()

  return (
    <GlobalContextProvider>
      <div className={classes.root}>
        <Router>
          <Drawer
            className={classes.drawer}
            variant="permanent"
            classes={{
              paper: classes.drawerPaper,
            }}
            anchor="left"
          >
            <div className={classes.toolbar} />
            <LateralMenu menuItems={menuItems} classes={classes}></LateralMenu>
          </Drawer>

          <Switch>
            <Route path="/dashboard">
              <Dashboard />
            </Route>
            <Route path="/job-creation">
              <JobCreation />
            </Route>
            <Route path="/">
              <Redirect to="/dashboard" />
            </Route>
          </Switch>
        </Router>
      </div>
    </GlobalContextProvider>
  );
}

export default App;

