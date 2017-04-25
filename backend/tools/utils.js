

function validate(email) {
  var tester = /^[-!#$%&'*+\/0-9=?A-Z^_a-z{|}~](\.?[-!#$%&'*+\/0-9=?A-Z^_a-z`{|}~])*@[a-zA-Z0-9](-?\.?[a-zA-Z0-9])*\.[a-zA-Z](-?[a-zA-Z0-9])+$/;
  if (!email) return false;

  if (email.length > 254) return false;
  
  var valid = tester.test(email);
  if(!valid) return false;
  
  var parts = email.split('@');
  if(parts[0].length > 64) return false;
  
  var domainParts = parts[1].split(".");
	if(domainParts.some(function(part) { return part.length > 63; }))
		return false;

	return true;
}

module.exports.validate = validate;