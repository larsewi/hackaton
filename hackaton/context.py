import json
import logging as log


def get_context(args):
    ctx = {"any": True}

    if args.build_type == "debug":
        log.debug('Setting context "debug" to True')
        ctx["debug"] = True
        log.debug('Setting context "release" to False')
        ctx["release"] = False
    elif args.build_type == "release":
        log.debug('Setting context "debug" to False')
        ctx["debug"] = False
        log.debug('Setting context "release" to True')
        ctx["release"] = True
    else:
        assert False, f"Illegal build type argument (--build-type={args.build_type})"
    assert (
        ctx["release"] != ctx["debug"]
    ), 'Context cannot have both "debug" and "release"'

    if args.project == "community":
        log.debug('Setting context "community" to True')
        ctx["community"] = True
        log.debug('Setting context "enterprise" to False')
        ctx["enterprise"] = False
    elif args.project == "enterprise":
        log.debug('Setting context "community" to False')
        ctx["community"] = False
        log.debug('Setting context "enterprise" to True')
        ctx["enterprise"] = True
    else:
        assert False, f"Illegal project argument (--project={args.project})"
    assert (
        ctx["community"] != ctx["enterprise"]
    ), 'Context cannot have both "community" and "enterprise"'

    if args.role == "agent":
        log.debug('Setting context "agent" to True')
        ctx["agent"] = True
        log.debug('Setting context "hub" to False')
        ctx["hub"] = False
    elif args.role == "hub":
        log.debug('Setting context "agent" to False')
        ctx["agent"] = False
        log.debug('Setting context "hub" to True')
        ctx["hub"] = True
    else:
        assert False, f"Illegal role argument (--role={args.role})"
    assert ctx["agent"] != ctx["hub"], 'Context cannot have both "agent" and "hub"'

    log.debug('Setting context "debian" to True')
    ctx["debian"] = True
    log.debug('Setting context "windows" to False')
    ctx["windows"] = False
    log.debug('Setting context "solaris" to False')
    ctx["solaris"] = False
    log.debug('Setting context "aix" to False')
    ctx["aix"] = False
    log.debug('Setting context "hpux" to False')
    ctx["hpux"] = False
    log.debug('Setting context "redhat" to False')
    ctx["redhat"] = False

    log.info(f"Current context:\n{json.dumps(ctx, indent=2)}")

    return ctx


def check_context(ctx, expression):
    return eval(expression, ctx)
