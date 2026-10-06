using Microsoft.Extensions.Configuration;
using System;
using System.Collections.Generic;
using System.Text;

namespace Comet.Services.FFXIV;

public class Universalis
{
    private readonly IConfiguration _config;
    public Universalis(IConfiguration config)
    {
        _config = config;
    }
}
