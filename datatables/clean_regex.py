def clean_regex(regex):
    """
    Escape any regex special characters other than alternation.

    :param regex: regex from datatables interface
    :type regex: str
    :rtype: str with regex to use with database
    """
    # copy for return
    ret_regex = regex

    # these characters are escaped (all except alternation | and escape \)
    # see http://www.regular-expressions.info/refquick.html
    escape_chars = '[^$.?*+(){}'

    # remove any escape chars
    ret_regex = ret_regex.replace('\\', '')

    # escape any characters which are used by regex
    # could probably concoct something incomprehensible using re.sub() but
    # prefer to write clear code with this loop
    # note expectation that no characters have already been escaped
    for c in escape_chars:
        ret_regex = ret_regex.replace(c, '\\' + c)

    # remove any double alternations until these don't exist any more
    while True:
        old_regex = ret_regex
        ret_regex = ret_regex.replace('||', '|')
        if old_regex == ret_regex:
            break

    # if last char is alternation | remove it because this
    # will cause operational error
    # this can happen as user is typing in global search box
    while len(ret_regex) >= 1 and ret_regex[-1] == '|':
        ret_regex = ret_regex[:-1]

    # and back to the caller
    return ret_regex
