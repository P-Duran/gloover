import React, { useState } from 'react';
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import { Collapse, Grid, IconButton, List, ListItem, ListItemText, Typography, withStyles } from '@material-ui/core';
import { StatusChip } from 'pages/Dashboard/Jobs/StatusChip'
import KeyboardArrowDownIcon from '@material-ui/icons/KeyboardArrowDown';
import { capitalizeFirstLetter } from 'pages/Dashboard/Jobs/Utils'
import KeyboardArrowUpIcon from '@material-ui/icons/KeyboardArrowUp';
import { GlooverButton } from 'components/GlooverButton';
import { removeJob } from 'model/jobsApi';
import { useSnackbar } from 'notistack';
import { ActiveJobStates } from 'utils/jobUtils';

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

export default function CollapsableRow({ row, id, header, importantCols, removeFromTable }) {
  const [open, setOpen] = useState(false);
  const { enqueueSnackbar } = useSnackbar();

  const renderCellContent = (row, column) => {
    if (row && column in row) {
      return (column === "state") ?
        <StatusChip label={row[column]} variant={row[column]} ></StatusChip> :
        <Typography variant="body2" noWrap>{row[column]}</Typography>
    }
    return ""
  }

  return <React.Fragment key={id}>
    <TableRow>
      {[...importantCols.map(column =>
        <StyledTableCell
          key={column + row[column]}
          size="small"
          scope="row"
          style={{ maxWidth: column === "id" ? -1 : 200, minWidth: column === "state" ? 150 : -1 }}>
          {renderCellContent(row, column)}
        </StyledTableCell>
      ),
      <StyledTableCell key={'last'} padding="checkbox">
        <IconButton aria-label="expand row" size="small" onClick={() => setOpen(!open)}>
          {open ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
        </IconButton>
      </StyledTableCell>]
      }
    </TableRow>
    <TableRow>
      <TableCell style={{ paddingBottom: 0, paddingTop: 0, border: 'none' }} colSpan={6}>
        <Collapse in={open} timeout="auto" unmountOnExit>
          <List>
            {[...header.map(h => !importantCols.includes(h) && h in row && <ListItem key={h}>
              <ListItemText
                key={h}
                primary={<Typography variant='body2' style={{ fontSize: 13, color: '#b0b0b0' }}>{capitalizeFirstLetter(h)}</Typography>}
                secondary={<Typography variant='body2' color={"textSecondary"} style={{ fontSize: 13 }}> {row[h].toString()}</Typography>}
              >
              </ListItemText>
            </ListItem>),
            <Grid key='Remove button' container justify='flex-end'>
              {ActiveJobStates.includes(row.state) &&
                <GlooverButton
                  variant='destructive'
                  label='Finish'
                  onClick={() => removeJob(row.id)
                    .then(data => {
                      removeFromTable(row.id);
                      enqueueSnackbar(`Job "${row.id}" was removed correctly`, {
                        variant: 'success',
                        autoHideDuration: 3000,
                      })
                    })
                    .catch(e =>
                      enqueueSnackbar(e.toString(), {
                        variant: 'success',
                        autoHideDuration: 3000,
                      })
                    )

                  } />}
            </Grid>]}
          </List>
        </Collapse>
      </TableCell>
    </TableRow>
  </React.Fragment>
}