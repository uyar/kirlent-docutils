# Copyright 2020-2021 H. Turgut Uyar <uyar@tekir.org>
#
# kirlent_docutils is released under the BSD license.
# Read the included LICENSE.txt file for details.


def modify_spec(spec, *, skip, overrides):
    options = []
    for option in spec[2]:
        key = option[1][0]
        if key in skip:
            continue

        key_overrides = overrides.get(key)
        if key_overrides is None:
            options.append(option)
            continue

        key_options = key_overrides.get("options", {})

        message_sub = key_overrides.get("message_sub")
        if message_sub is None:
            message = option[0]
        else:
            message = message_sub[0].sub(r"\1%s" % message_sub[1], option[0])

        options.append((message, option[1], {**option[2], **key_options}))

    return tuple(options)
