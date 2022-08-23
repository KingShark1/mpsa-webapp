def get_age_group_from_birthyear(birthyear: int) -> str:
	if birthyear < 2005:
		return 'Senior'
	elif birthyear >= 2005 and birthyear < 2008:
		return 'I'
	elif birthyear >=2008 and birthyear < 2010:
		return 'II'

