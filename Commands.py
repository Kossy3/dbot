import re
import types
from inspect import signature, Parameter
from typing import Any
from Message import *

class Commands:
    class Command:
        def __init__(self, func: types.FunctionType, help: str):
            self.func: types.FunctionType = func
            self.help = help
        async def __call__(self, message, args):
            return await self.func(message, args)
            
    class RegixCommand:
        def __init__(self, func: types.FunctionType, pattern: re.Pattern):
            self.func = func
            self.pattern: re.Pattern = pattern
        async def __call__(self, **kwargs):
            return await self.func(**kwargs)

    class MissingArgument(Exception):
        ...

    def __init__(self, prefix = ''):
        self.prefix = prefix
        self.commands: dict[str, Commands.Command] = {}
        self.regix_commands: list[Commands.RegixCommand] = []

    def command(self, name=[], help=""):
        def deco(func: types.FunctionType):
            func_args = func.__code__.co_varnames[:func.__code__.co_argcount]
            sig = signature(func)

            # 引数をアノテーションの型に自動変換
            def convert_args(key, value):
                if sig.parameters[key].annotation == Parameter.empty:
                  return value
                else:
                  try:
                      return sig.parameters[key].annotation(value)
                  except TypeError: 
                      return sig.parameters[key].annotation()
                  except ValueError:
                      return sig.parameters[key].annotation()
                  
            async def new_func(message, args):
                sp_kwargs = {
                    "message": message
                }
                if len([k for k in func_args if k not in sp_kwargs]) > len(args):
                    raise Commands.MissingArgument
                iter_args = iter(args)
                new_kwargs = {
                    k: sp_kwargs[k] if k in sp_kwargs else convert_args(k, next(iter_args)) for k in func_args 
                }
                return await func(**new_kwargs)
                
            if not name:
                self.commands[func.__name__] = Commands.Command(new_func, help)
            for n in name:
                self.commands[n] = Commands.Command(new_func, help)
            return new_func
        return deco
        
    def regix_command(self, regix=r'^.*$'):
        def deco(func: types.FunctionType):
            func_args = func.__code__.co_varnames[:func.__code__.co_argcount]
            async def new_func(**kwargs):
                await func(**{k:kwargs[k] for k in func_args})
            pattern = re.compile(regix)
            self.regix_commands.append(Commands.RegixCommand(new_func, pattern))
            return new_func
        return deco

    async def call_commands(self, message: Message):
        args = message.content.split()
        cmd_name = re.search(rf'^{self.prefix}(.+)$', args[0])
        if cmd_name and cmd_name[1] in self.commands:
            return await self.commands[cmd_name[1]](message, args[1:])
        for cmd in self.regix_commands:
            if cmd.pattern.search(message.content):
                return await cmd(message = message)
        return None
