import React, { useContext, useEffect, useState } from 'react';
import { makeStyles, withStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import { Box, CircularProgress, Grid, Toolbar, Typography } from '@material-ui/core';
import { capitalizeFirstLetter } from 'pages/Dashboard/Jobs/Utils'
import CollapsableRow from 'pages/Dashboard/Jobs/CollapsableRow'
import { GlobalContext } from 'context/GlobalContext';

const useStyles = makeStyles({
  table: {
    minWidth: 650,
    overflow: "hidden",
  },
  tableContainer: {
    padding: 10,
    overflow: "hidden"
  }
});

const StyledTableCell = withStyles((theme) => ({
  body: {
    fontSize: 14,
    borderBottom: "none",
    paddingTop: 10
  },
  head: {
    fontSize: 14,
    backgroundColor: "#f4f6f8",
    color: "#637381",
    borderBottom: "none"
  }
}))(TableCell);

const importantCols = ["id", "trigger", "trigger_time", "state", "spider"]


export default function JobTable({ main = false, tableTitle = 'Job Table', filterJobs = (job) => true }) {
  const classes = useStyles();
  const [header, setHeader] = useState();
  const { jobs } = useContext(GlobalContext);

  useEffect(() => {
    updateHeader(jobs)
  }, [jobs])

  const removeFromTable = (id) => {
    delete jobs[id]
    updateHeader(jobs)
  }
  const filteredJobs = (jobsToFilter) => {
    const tmpJobs = { ...jobsToFilter }
    Object.values(tmpJobs).forEach(job => !filterJobs(job) && delete tmpJobs[job.id])
    return tmpJobs;
  }
  const updateHeader = (tmpJobs) => {
    if (Object.values(tmpJobs).length > 0)
      setHeader([...new Set(Object.values(tmpJobs).map(job => Object.keys(job)).flat())]);
    else setHeader([])
  }

  const getRows = () => {
    return Object.values(filteredJobs(jobs)).map((row, i) =>
      <CollapsableRow key={i} row={row} id={i} header={header} importantCols={importantCols} removeFromTable={removeFromTable}>
      </CollapsableRow>
    )
  }

  const getHeader = () => {
    if (!header) {
      return <Grid container justify='center' > <CircularProgress style={{ color: 'black' }} /></Grid>
    }
    if (header.length > 0) {
      return <TableRow key={'headerRow'}>
        {[...importantCols.map((col, i) =>
          <StyledTableCell
            key={col + i}
            style={{
              borderBottomLeftRadius: i === 0 ? 16 : 0,
              borderTopLeftRadius: i === 0 ? 16 : 0
            }}>
            {capitalizeFirstLetter(col)}
          </StyledTableCell>),
        <StyledTableCell key={'last'} padding="checkbox" style={{
          borderBottomRightRadius: 16,
          borderTopRightRadius: 16
        }}>
        </StyledTableCell>]
        }
      </TableRow>
    } else {
      return <Grid container justify='center'>There are no jobs here 😓</Grid>
    }
  }


  return (
    (header && Object.keys(filteredJobs(jobs)).length > 0 | main) ? (<TableContainer className={classes.tableContainer}>
      <Box boxShadow={3} borderRadius={16} padding={2}>
        <Table className={classes.table} aria-label="simple table">
          <TableHead>
            <Toolbar>
              <Typography variant="h6" id="tableTitle" component="div">
                {tableTitle}
              </Typography>
            </Toolbar>
            {getHeader()}
          </TableHead>
          <TableBody>
            {header && getRows()}
          </TableBody>
        </Table>
      </Box>
    </TableContainer>) : ""
  );
}
