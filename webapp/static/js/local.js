function statusFormatter(value, row, index) {
   return value;
   return [
        '<span class="badge badge-info">' + value + '</span>'
    ].join('');
}


function categoryFormatter(value, row, index) {
//    value = value.toLowerCase();
   if (value === 'threat')
       return '<span class="big-badge badge badge-danger">' + value + '</span>';
   if (value === 'clean')
       return '<span class="big-badge badge badge-success">' + value + '</span>';
   if (value === 'spam')
       return '<span class="big-badge badge badge-warning">' + value + '</span>';
   if (value === 'unknown')
       return '<span class="big-badge badge badge-secondary">' + value + '</span>';
}

function reported_byFormatter(value, row, index) {
   return [
        '<span class="badge badge-warning">2 users </span>'
    ].join('');
}


function hasattachment(value,row) {
  if (value === true )
    return '<i class="fas fa-paperclip"></i>';
  if (value !== true )
    return '';
}


function caseFormatter(value, row) {
  return "<a  href='/email/"+ row.id + "' >" + value +  "</a>";
}







function dateFormatter(value, row) {
  return dateCommonFormatter(value,row,"YYYY-MM-DD");
}

function dateTimeFormatter(value, row) {
  return dateCommonFormatter(value,row,"YYYY-MM-DD hh:mm:ss");
}
function dateCommonFormatter(value,row,format) {
    if(value == null) {
      return "NA";
    }
    var utc_date = moment.utc(value);
    if (!utc_date.isValid() && value.length>10) {
        // Attempt to insert a space
        newDate = value.substring(0,10) + " " + value.substring(10,value.length)
        utc_date = moment.utc(newDate)
    }
    var local_date = moment(utc_date).local()

    return local_date.format(format);
}

function rowStyle(row, index) {
  if (row.seen) {
    return {css: {"font-weight": "normal"} };
  }
    return {css: {"font-weight": "bold"} };
}

function subjectFormatter(value, row) {
       return "<a  href='/email/"+ row.id + "' >" + value +  "</a>";
}

function tagsFormatter(value, row) {


 var tags = '';
 $.each(value.split(','), function( index, value ) {
    tags += ' <span class="badge bg-info">'+ value +'</span> ';
 });
 return tags;
}

function obserableFormatter(value, row) {
 var count =  value['emails'].length +  value['ips'].length + value['urls'].length ;
 return count;
}

function productImageFormatter(value, row) {
  return "<img src='/static/images/uploads/" + value + "' width='50px'>";
}



function toolTipURLFormatter(value, row) {
  return "<div data-toggle='tooltip' data-placement='top' title='"+value.domain+"'>"+value.domain+"</div>";
}









